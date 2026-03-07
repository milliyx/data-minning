"""Silver to Gold ETL pipeline."""

from pathlib import Path
from typing import Dict, Any

from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from pyspark.sql.window import Window

from ..common.io import read_parquet_snapshot, write_parquet_snapshot


def build_fact_usage_daily(
    usage_logs_df: DataFrame,
) -> DataFrame:
    """
    Build daily usage facts aggregated by user and date.
    
    Args:
        usage_logs_df: Cleaned usage logs
        
    Returns:
        Daily usage facts DataFrame
    """
    return (
        usage_logs_df
        .groupBy('user_id', 'date')
        .agg(
            F.sum('sessions').alias('sessions'),
            F.sum('minutes').alias('minutes'),
            F.sum(
                F.col('feature_a') + F.col('feature_b') + F.col('feature_c')
            ).alias('features_used_count'),
        )
        .orderBy('user_id', 'date')
    )


def build_fact_revenue_daily(
    payments_df: DataFrame,
) -> DataFrame:
    """
    Build daily revenue facts aggregated by user and date.
    
    Args:
        payments_df: Cleaned payments
        
    Returns:
        Daily revenue facts DataFrame
    """
    return (
        payments_df
        .groupBy('user_id', 'date')
        .agg(
            F.sum(
                F.when(F.col('success'), F.col('amount')).otherwise(0)
            ).alias('revenue'),
            F.sum(
                F.when(~F.col('success'), 1).otherwise(0)
            ).alias('payment_failures'),
        )
        .orderBy('user_id', 'date')
    )


def build_churn_features(
    users_df: DataFrame,
    subscriptions_df: DataFrame,
    usage_daily_df: DataFrame,
    payments_daily_df: DataFrame,
    events_df: DataFrame,
    as_of_date: str,
) -> DataFrame:
    """
    Build churn prediction features.
    
    Args:
        users_df: Users table
        subscriptions_df: Subscriptions table
        usage_daily_df: Daily usage facts
        payments_daily_df: Daily revenue facts
        events_df: Events table
        as_of_date: Date to compute features as of
        
    Returns:
        Churn features DataFrame
    """
    from datetime import datetime, timedelta
    
    as_of_dt = datetime.strptime(as_of_date, '%Y-%m-%d')
    date_7d = (as_of_dt - timedelta(days=7)).strftime('%Y-%m-%d')
    date_30d = (as_of_dt - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # Get active users as of date
    active_users = (
        subscriptions_df
        .filter(F.col('status') == 'active')
        .select('user_id', 'plan')
    )
    
    # Usage features (last 7 and 30 days)
    usage_7d = (
        usage_daily_df
        .filter((F.col('date') >= date_7d) & (F.col('date') <= as_of_date))
        .groupBy('user_id')
        .agg(
            F.sum('minutes').alias('last_7d_minutes'),
            F.sum('sessions').alias('last_7d_sessions'),
        )
    )
    
    usage_30d = (
        usage_daily_df
        .filter((F.col('date') >= date_30d) & (F.col('date') <= as_of_date))
        .groupBy('user_id')
        .agg(
            F.sum('minutes').alias('last_30d_minutes'),
            F.sum('sessions').alias('last_30d_sessions'),
        )
    )
    
    # Payment failure rate (last 30 days)
    payment_stats = (
        payments_daily_df
        .filter((F.col('date') >= date_30d) & (F.col('date') <= as_of_date))
        .groupBy('user_id')
        .agg(
            F.sum('payment_failures').alias('payment_failures_30d'),
            F.count('*').alias('payment_attempts_30d'),
        )
        .withColumn(
            'payment_fail_rate_30d',
            F.when(
                F.col('payment_attempts_30d') > 0,
                F.col('payment_failures_30d') / F.col('payment_attempts_30d')
            ).otherwise(0)
        )
        .select('user_id', 'payment_fail_rate_30d')
    )
    
    # Tenure
    user_tenure = (
        users_df
        .select(
            'user_id',
            F.datediff(F.lit(as_of_date), F.col('signup_date')).alias('tenure_days')
        )
    )
    
    # Promo and outage exposure (last 30 days)
    promo_count = (
        events_df
        .filter(
            (F.col('event_type') == 'promo') &
            (F.col('date') >= date_30d) &
            (F.col('date') <= as_of_date)
        )
        .count()
    )
    
    outage_count = (
        events_df
        .filter(
            (F.col('event_type') == 'outage') &
            (F.col('date') >= date_30d) &
            (F.col('date') <= as_of_date)
        )
        .count()
    )
    
    # Join all features
    features = (
        active_users
        .join(usage_7d, 'user_id', 'left')
        .join(usage_30d, 'user_id', 'left')
        .join(payment_stats, 'user_id', 'left')
        .join(user_tenure, 'user_id', 'left')
        .fillna(0, subset=[
            'last_7d_minutes', 'last_7d_sessions',
            'last_30d_minutes', 'last_30d_sessions',
            'payment_fail_rate_30d',
        ])
        .withColumn('as_of_date', F.lit(as_of_date))
        .withColumn('promo_exposure_30d', F.lit(promo_count))
        .withColumn('outage_exposure_30d', F.lit(outage_count))
    )
    
    return features


def build_churn_labels(
    subscriptions_df: DataFrame,
    as_of_date: str,
    lookahead_days: int = 30,
) -> DataFrame:
    """
    Build churn labels (1 if churned within lookahead period).
    
    Args:
        subscriptions_df: Subscriptions table
        as_of_date: Date to compute labels as of
        lookahead_days: Days to look ahead for churn
        
    Returns:
        Churn labels DataFrame
    """
    from datetime import datetime, timedelta
    
    as_of_dt = datetime.strptime(as_of_date, '%Y-%m-%d')
    future_date = (as_of_dt + timedelta(days=lookahead_days)).strftime('%Y-%m-%d')
    
    # Users who were active as of date
    active_as_of = (
        subscriptions_df
        .filter(
            (F.col('start_date') <= as_of_date) &
            ((F.col('end_date').isNull()) | (F.col('end_date') > as_of_date))
        )
        .select('user_id')
        .distinct()
    )
    
    # Users who churned within lookahead period
    churned = (
        subscriptions_df
        .filter(
            (F.col('status') == 'cancelled') &
            (F.col('end_date') > as_of_date) &
            (F.col('end_date') <= future_date)
        )
        .select('user_id')
        .distinct()
        .withColumn('label', F.lit(1))
    )
    
    # Join and fill non-churners with 0
    labels = (
        active_as_of
        .join(churned, 'user_id', 'left')
        .fillna(0, subset=['label'])
        .withColumn('label_date', F.lit(as_of_date))
    )
    
    return labels


def build_kpis(
    users_df: DataFrame,
    subscriptions_df: DataFrame,
    revenue_daily_df: DataFrame,
) -> DataFrame:
    """
    Build daily KPIs.
    
    Args:
        users_df: Users table
        subscriptions_df: Subscriptions table
        revenue_daily_df: Daily revenue facts
        
    Returns:
        Daily KPIs DataFrame
    """
    # ARPU (Average Revenue Per User) by date
    arpu = (
        revenue_daily_df
        .groupBy('date')
        .agg(
            F.avg('revenue').alias('arpu'),
            F.sum('revenue').alias('total_revenue'),
            F.count('user_id').alias('active_users'),
        )
    )
    
    return arpu.orderBy('date')


def silver_to_gold_pipeline(
    spark: SparkSession,
    silver_path: Path,
    gold_path: Path,
    run_date: str,
) -> None:
    """
    Execute Silver to Gold ETL pipeline.
    
    Args:
        spark: SparkSession
        silver_path: Silver layer base path
        gold_path: Gold layer base path
        run_date: Run date in YYYY-MM-DD format
    """
    print(f"\n{'='*60}")
    print(f"SILVER → GOLD ETL PIPELINE")
    print(f"Run Date: {run_date}")
    print(f"{'='*60}\n")
    
    # Read Silver tables
    print("Reading Silver layer...")
    users_df = read_parquet_snapshot(spark, silver_path, 'users', run_date)
    subscriptions_df = read_parquet_snapshot(spark, silver_path, 'subscriptions', run_date)
    payments_df = read_parquet_snapshot(spark, silver_path, 'payments', run_date)
    usage_logs_df = read_parquet_snapshot(spark, silver_path, 'usage_logs', run_date)
    events_df = read_parquet_snapshot(spark, silver_path, 'events', run_date)
    
    # Build fact tables
    print("\nBuilding fact tables...")
    fact_usage_daily = build_fact_usage_daily(usage_logs_df)
    fact_revenue_daily = build_fact_revenue_daily(payments_df)
    
    # Build churn features and labels
    print("Building churn features and labels...")
    churn_features = build_churn_features(
        users_df,
        subscriptions_df,
        fact_usage_daily,
        fact_revenue_daily,
        events_df,
        run_date,
    )
    churn_labels = build_churn_labels(subscriptions_df, run_date)
    
    # Build KPIs
    print("Building KPIs...")
    kpis = build_kpis(users_df, subscriptions_df, fact_revenue_daily)
    
    # Write Gold tables
    print("\nWriting Gold layer...")
    tables = {
        'fact_usage_daily': fact_usage_daily,
        'fact_revenue_daily': fact_revenue_daily,
        'churn_features': churn_features,
        'churn_labels': churn_labels,
        'kpis_daily': kpis,
    }
    
    for table_name, df in tables.items():
        write_parquet_snapshot(df, gold_path, table_name, run_date)
        count = df.count()
        print(f"  {table_name}: {count:,} rows")
    
    print(f"\n✓ Gold layer created successfully at: {gold_path}")
