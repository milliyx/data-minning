"""Data generation module for Bronze layer."""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List
import uuid

from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F

from .schemas import (
    USERS_SCHEMA,
    SUBSCRIPTIONS_SCHEMA,
    PAYMENTS_SCHEMA,
    USAGE_LOGS_SCHEMA,
    EVENTS_SCHEMA,
)
from .logic import SimulationEngine
from ..common.io import write_parquet_snapshot


class DataGenerator:
    """
    Deterministic data generator for the subscription platform simulation.
    
    Given the same seed and configuration, generates identical datasets.
    """
    
    def __init__(
        self,
        spark: SparkSession,
        config: Dict[str, Any],
        seed: int,
        run_date: str,
        output_path: Path,
    ):
        """
        Initialize data generator.
        
        Args:
            spark: SparkSession
            config: Simulation configuration
            seed: Random seed
            run_date: Run date for snapshot
            output_path: Base path for Bronze layer
        """
        self.spark = spark
        self.config = config
        self.seed = seed
        self.run_date = run_date
        self.output_path = output_path
        self.engine = SimulationEngine(config, seed)
        
        # Parse run_date
        self.run_date_dt = datetime.strptime(run_date, "%Y-%m-%d")
        
    def generate_all(self) -> Dict[str, DataFrame]:
        """
        Generate all Bronze layer tables.
        
        Returns:
            Dictionary mapping table names to DataFrames
        """
        print(f"Generating data with seed {self.seed} for run_date {self.run_date}")
        
        # Calculate simulation period
        months = self.config['months_history']
        start_date = self.run_date_dt - timedelta(days=months * 30)
        
        # Generate tables in dependency order
        users_df = self.generate_users(start_date)
        events_df = self.generate_events(start_date)
        subscriptions_df = self.generate_subscriptions(users_df, start_date)
        payments_df = self.generate_payments(users_df, subscriptions_df, events_df, start_date)
        usage_logs_df = self.generate_usage_logs(users_df, subscriptions_df, events_df, start_date)
        
        # Write to Bronze layer
        tables = {
            'users': users_df,
            'subscriptions': subscriptions_df,
            'payments': payments_df,
            'usage_logs': usage_logs_df,
            'events': events_df,
        }
        
        for table_name, df in tables.items():
            write_parquet_snapshot(df, self.output_path, table_name, self.run_date)
            count = df.count()
            print(f"  {table_name}: {count:,} rows")
        
        return tables
    
    def generate_users(self, start_date: datetime) -> DataFrame:
        """Generate users table."""
        n_users = self.config['population_size']
        
        # Generate signup dates
        signup_dates = self.engine.generate_signup_dates(
            n_users,
            start_date,
            self.run_date_dt,
        )
        
        # Generate demographics
        ages, cities, channels = self.engine.assign_demographics(n_users)
        
        # Create user records
        users = []
        for i in range(n_users):
            users.append({
                'user_id': f'U{i+1:08d}',
                'signup_date': signup_dates[i].date(),
                'age': ages[i],
                'city': cities[i],
                'acquisition_channel': channels[i],
            })
        
        return self.spark.createDataFrame(users, schema=USERS_SCHEMA)
    
    def generate_events(self, start_date: datetime) -> DataFrame:
        """Generate business events table."""
        events = []
        event_id = 1
        
        # Generate outages
        outage_rate = self.config['outage_rate']
        months = self.config['months_history']
        n_outages = int(outage_rate * months)
        
        for _ in range(n_outages):
            event_date = start_date + timedelta(
                days=int(self.engine.rng.uniform(0, months * 30))
            )
            events.append({
                'event_id': f'E{event_id:06d}',
                'date': event_date.date(),
                'event_type': 'outage',
                'intensity': self.engine.rng.uniform(0.3, 1.0),
                'affected_segment': None,
            })
            event_id += 1
        
        # Generate promotions (monthly)
        for month in range(months):
            event_date = start_date + timedelta(days=month * 30 + 15)
            segment = self.engine.rng.choice(['all', 'basic', 'standard', 'premium'])
            events.append({
                'event_id': f'E{event_id:06d}',
                'date': event_date.date(),
                'event_type': 'promo',
                'intensity': self.engine.rng.uniform(0.5, 1.0),
                'affected_segment': segment,
            })
            event_id += 1
        
        return self.spark.createDataFrame(events, schema=EVENTS_SCHEMA)
    
    def generate_subscriptions(
        self,
        users_df: DataFrame,
        start_date: datetime,
    ) -> DataFrame:
        """Generate subscriptions table."""
        users = users_df.collect()
        subscriptions = []
        sub_id = 1
        
        plans = self.engine.assign_plans(len(users))
        
        for i, user_row in enumerate(users):
            user_id = user_row['user_id']
            signup_date = user_row['signup_date']
            plan = plans[i]
            
            # Initial subscription
            subscriptions.append({
                'subscription_id': f'S{sub_id:08d}',
                'user_id': user_id,
                'plan': plan,
                'start_date': signup_date,
                'end_date': None,
                'status': 'active',
            })
            sub_id += 1
        
        return self.spark.createDataFrame(subscriptions, schema=SUBSCRIPTIONS_SCHEMA)
    
    def generate_payments(
        self,
        users_df: DataFrame,
        subscriptions_df: DataFrame,
        events_df: DataFrame,
        start_date: datetime,
    ) -> DataFrame:
        """Generate payments table."""
        users = users_df.collect()
        subs = {s['user_id']: s for s in subscriptions_df.collect()}
        events_list = events_df.collect()
        
        # Build outage dates set
        outage_dates = {
            e['date'] for e in events_list if e['event_type'] == 'outage'
        }
        
        payments = []
        payment_id = 1
        
        plan_prices = self.config['plan_prices']
        payment_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer']
        
        for user_row in users:
            user_id = user_row['user_id']
            signup_date = user_row['signup_date']
            
            if user_id not in subs:
                continue
            
            plan = subs[user_id]['plan']
            price = plan_prices[plan]
            
            # Generate monthly payments from signup to run_date
            current_date = signup_date
            while current_date <= self.run_date_dt.date():
                # Check if outage in last 7 days
                outage_active = any(
                    abs((current_date - od).days) <= 7
                    for od in outage_dates
                )
                
                success = self.engine.compute_payment_success(
                    self.config['payment_fail_base'],
                    self.config['price_sensitivity'],
                    price,
                    outage_active,
                )
                
                # Add some time variance
                payment_time = datetime.combine(
                    current_date,
                    datetime.min.time()
                ) + timedelta(
                    hours=int(self.engine.rng.uniform(0, 24)),
                    minutes=int(self.engine.rng.uniform(0, 60)),
                )
                
                payments.append({
                    'payment_id': f'P{payment_id:010d}',
                    'user_id': user_id,
                    'ts': payment_time,
                    'amount': price,
                    'method': self.engine.rng.choice(payment_methods),
                    'success': success,
                })
                payment_id += 1
                
                # Next month
                current_date = (
                    datetime.combine(current_date, datetime.min.time())
                    + timedelta(days=30)
                ).date()
        
        return self.spark.createDataFrame(payments, schema=PAYMENTS_SCHEMA)
    
    def generate_usage_logs(
        self,
        users_df: DataFrame,
        subscriptions_df: DataFrame,
        events_df: DataFrame,
        start_date: datetime,
    ) -> DataFrame:
        """Generate usage logs table."""
        users = users_df.collect()
        subs = {s['user_id']: s for s in subscriptions_df.collect()}
        events_list = events_df.collect()
        
        # Build promo and outage date sets
        promo_dates = {
            e['date'] for e in events_list if e['event_type'] == 'promo'
        }
        outage_dates = {
            e['date'] for e in events_list if e['event_type'] == 'outage'
        }
        
        logs = []
        log_id = 1
        
        for user_row in users:
            user_id = user_row['user_id']
            signup_date = user_row['signup_date']
            
            if user_id not in subs:
                continue
            
            plan = subs[user_id]['plan']
            
            # Generate daily logs from signup to run_date
            current_date = signup_date
            while current_date <= self.run_date_dt.date():
                # Randomly skip some days (not all users use every day)
                if self.engine.rng.random() > 0.7:  # 70% activity rate
                    current_date = (
                        datetime.combine(current_date, datetime.min.time())
                        + timedelta(days=1)
                    ).date()
                    continue
                
                day_of_week = current_date.weekday()
                promo_active = current_date in promo_dates
                outage_active = current_date in outage_dates
                
                sessions, minutes = self.engine.compute_usage_level(
                    plan,
                    day_of_week,
                    promo_active,
                    outage_active,
                    self.config['seasonality_strength'],
                )
                
                # Random feature usage
                feature_a = int(self.engine.rng.poisson(2) if sessions > 0 else 0)
                feature_b = int(self.engine.rng.poisson(1) if sessions > 0 else 0)
                feature_c = int(self.engine.rng.poisson(0.5) if sessions > 0 else 0)
                
                # Random time during the day
                log_time = datetime.combine(
                    current_date,
                    datetime.min.time()
                ) + timedelta(
                    hours=int(self.engine.rng.uniform(6, 23)),
                    minutes=int(self.engine.rng.uniform(0, 60)),
                )
                
                logs.append({
                    'log_id': f'L{log_id:012d}',
                    'user_id': user_id,
                    'ts': log_time,
                    'sessions': sessions,
                    'minutes': minutes,
                    'feature_a': feature_a,
                    'feature_b': feature_b,
                    'feature_c': feature_c,
                })
                log_id += 1
                
                current_date = (
                    datetime.combine(current_date, datetime.min.time())
                    + timedelta(days=1)
                ).date()
        
        return self.spark.createDataFrame(logs, schema=USAGE_LOGS_SCHEMA)


def generate_bronze_data(
    spark: SparkSession,
    config: Dict[str, Any],
    team_id: str,
    seed: int,
    run_date: str,
    output_base: Path,
) -> None:
    """
    Main entry point for data generation.
    
    Args:
        spark: SparkSession
        config: Full configuration dictionary
        team_id: Team identifier
        seed: Random seed
        run_date: Run date in YYYY-MM-DD format
        output_base: Base output path
    """
    print(f"\n{'='*60}")
    print(f"BRONZE LAYER DATA GENERATION")
    print(f"Team: {team_id}")
    print(f"Seed: {seed}")
    print(f"Run Date: {run_date}")
    print(f"{'='*60}\n")
    
    bronze_path = output_base / "bronze"
    
    generator = DataGenerator(
        spark=spark,
        config=config['simulation'],
        seed=seed,
        run_date=run_date,
        output_path=bronze_path,
    )
    
    generator.generate_all()
    
    print(f"\nBronze data generated successfully at: {bronze_path}")
