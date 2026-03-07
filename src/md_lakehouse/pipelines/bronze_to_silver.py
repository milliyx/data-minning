"""Bronze to Silver ETL pipeline."""

from pathlib import Path
from typing import Dict, Any

from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from pyspark.sql.window import Window

from ..common.io import read_parquet_snapshot, write_parquet_snapshot
from .quality import (
    NotNullCheck,
    RangeCheck,
    UniqueCheck,
    ReferentialIntegrityCheck,
    run_quality_checks,
    print_quality_report,
)


def clean_users(df: DataFrame) -> DataFrame:
    """
    Clean users table.
    
    Args:
        df: Raw users DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    return (
        df
        # Remove duplicates (keep first by signup_date)
        .withColumn(
            'row_num',
            F.row_number().over(
                Window.partitionBy('user_id').orderBy('signup_date')
            )
        )
        .filter(F.col('row_num') == 1)
        .drop('row_num')
        # Standardize city names
        .withColumn('city', F.initcap(F.trim(F.col('city'))))
        # Ensure age is within bounds
        .filter((F.col('age') >= 14) & (F.col('age') <= 90))
    )


def clean_subscriptions(df: DataFrame) -> DataFrame:
    """
    Clean subscriptions table.
    
    Args:
        df: Raw subscriptions DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    return (
        df
        # Remove duplicates (keep first by start_date)
        .withColumn(
            'row_num',
            F.row_number().over(
                Window.partitionBy('subscription_id').orderBy('start_date')
            )
        )
        .filter(F.col('row_num') == 1)
        .drop('row_num')
        # Validate date logic
        .filter(
            F.col('end_date').isNull() |
            (F.col('end_date') >= F.col('start_date'))
        )
        # Standardize plan names
        .withColumn('plan', F.lower(F.trim(F.col('plan'))))
        .withColumn('status', F.lower(F.trim(F.col('status'))))
    )


def clean_payments(df: DataFrame) -> DataFrame:
    """
    Clean payments table.
    
    Args:
        df: Raw payments DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    return (
        df
        # Remove duplicates
        .withColumn(
            'row_num',
            F.row_number().over(
                Window.partitionBy('payment_id').orderBy('ts')
            )
        )
        .filter(F.col('row_num') == 1)
        .drop('row_num')
        # Ensure positive amounts
        .filter(F.col('amount') > 0)
        # Normalize timestamp to UTC
        .withColumn('date', F.to_date(F.col('ts')))
    )


def clean_usage_logs(df: DataFrame) -> DataFrame:
    """
    Clean usage logs table.
    
    Args:
        df: Raw usage logs DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    return (
        df
        # Remove duplicates
        .withColumn(
            'row_num',
            F.row_number().over(
                Window.partitionBy('log_id').orderBy('ts')
            )
        )
        .filter(F.col('row_num') == 1)
        .drop('row_num')
        # Ensure non-negative metrics
        .filter(
            (F.col('sessions') >= 0) &
            (F.col('minutes') >= 0) &
            (F.col('feature_a') >= 0) &
            (F.col('feature_b') >= 0) &
            (F.col('feature_c') >= 0)
        )
        # Add date column
        .withColumn('date', F.to_date(F.col('ts')))
    )


def clean_events(df: DataFrame) -> DataFrame:
    """
    Clean events table.
    
    Args:
        df: Raw events DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    return (
        df
        # Remove duplicates
        .withColumn(
            'row_num',
            F.row_number().over(
                Window.partitionBy('event_id').orderBy('date')
            )
        )
        .filter(F.col('row_num') == 1)
        .drop('row_num')
        # Standardize event types
        .withColumn('event_type', F.lower(F.trim(F.col('event_type'))))
        # Ensure intensity is in valid range
        .filter((F.col('intensity') >= 0) & (F.col('intensity') <= 1))
    )


def validate_silver_quality(
    users_df: DataFrame,
    subscriptions_df: DataFrame,
    payments_df: DataFrame,
    usage_logs_df: DataFrame,
    events_df: DataFrame,
) -> bool:
    """
    Run quality checks on all Silver tables.
    
    Args:
        All Silver DataFrames
        
    Returns:
        True if all checks passed
    """
    all_passed = True
    
    # Users quality checks
    users_checks = [
        NotNullCheck(['user_id', 'signup_date', 'age', 'city', 'acquisition_channel']),
        UniqueCheck(['user_id']),
        RangeCheck('age', 14, 90),
    ]
    users_results = run_quality_checks('users', users_df, users_checks)
    print_quality_report(users_results)
    all_passed = all_passed and users_results['all_passed']
    
    # Subscriptions quality checks
    subs_checks = [
        NotNullCheck(['subscription_id', 'user_id', 'plan', 'start_date', 'status']),
        UniqueCheck(['subscription_id']),
        ReferentialIntegrityCheck(
            'subscriptions', 'user_id',
            users_df, 'user_id'
        ),
    ]
    subs_results = run_quality_checks('subscriptions', subscriptions_df, subs_checks)
    print_quality_report(subs_results)
    all_passed = all_passed and subs_results['all_passed']
    
    # Payments quality checks
    payments_checks = [
        NotNullCheck(['payment_id', 'user_id', 'ts', 'amount', 'method', 'success']),
        UniqueCheck(['payment_id']),
        RangeCheck('amount', 0.01, 1000),
        ReferentialIntegrityCheck(
            'payments', 'user_id',
            users_df, 'user_id'
        ),
    ]
    payments_results = run_quality_checks('payments', payments_df, payments_checks)
    print_quality_report(payments_results)
    all_passed = all_passed and payments_results['all_passed']
    
    # Usage logs quality checks
    usage_checks = [
        NotNullCheck(['log_id', 'user_id', 'ts', 'sessions', 'minutes']),
        UniqueCheck(['log_id']),
        RangeCheck('sessions', 0, 100),
        RangeCheck('minutes', 0, 1440),
        ReferentialIntegrityCheck(
            'usage_logs', 'user_id',
            users_df, 'user_id'
        ),
    ]
    usage_results = run_quality_checks('usage_logs', usage_logs_df, usage_checks)
    print_quality_report(usage_results)
    all_passed = all_passed and usage_results['all_passed']
    
    # Events quality checks
    events_checks = [
        NotNullCheck(['event_id', 'date', 'event_type', 'intensity']),
        UniqueCheck(['event_id']),
        RangeCheck('intensity', 0, 1),
    ]
    events_results = run_quality_checks('events', events_df, events_checks)
    print_quality_report(events_results)
    all_passed = all_passed and events_results['all_passed']
    
    return all_passed


def bronze_to_silver_pipeline(
    spark: SparkSession,
    bronze_path: Path,
    silver_path: Path,
    run_date: str,
) -> None:
    """
    Execute Bronze to Silver ETL pipeline.
    
    Args:
        spark: SparkSession
        bronze_path: Bronze layer base path
        silver_path: Silver layer base path
        run_date: Run date in YYYY-MM-DD format
    """
    print(f"\n{'='*60}")
    print(f"BRONZE → SILVER ETL PIPELINE")
    print(f"Run Date: {run_date}")
    print(f"{'='*60}\n")
    
    # Read Bronze tables
    print("Reading Bronze layer...")
    users_bronze = read_parquet_snapshot(spark, bronze_path, 'users', run_date)
    subscriptions_bronze = read_parquet_snapshot(spark, bronze_path, 'subscriptions', run_date)
    payments_bronze = read_parquet_snapshot(spark, bronze_path, 'payments', run_date)
    usage_logs_bronze = read_parquet_snapshot(spark, bronze_path, 'usage_logs', run_date)
    events_bronze = read_parquet_snapshot(spark, bronze_path, 'events', run_date)
    
    # Clean tables
    print("\nCleaning tables...")
    users_silver = clean_users(users_bronze)
    subscriptions_silver = clean_subscriptions(subscriptions_bronze)
    payments_silver = clean_payments(payments_bronze)
    usage_logs_silver = clean_usage_logs(usage_logs_bronze)
    events_silver = clean_events(events_bronze)
    
    # Validate quality
    print("\n" + "="*60)
    print("QUALITY VALIDATION")
    print("="*60)
    
    quality_passed = validate_silver_quality(
        users_silver,
        subscriptions_silver,
        payments_silver,
        usage_logs_silver,
        events_silver,
    )
    
    if not quality_passed:
        raise ValueError("Quality checks failed! Silver layer not written.")
    
    # Write Silver tables
    print("\nWriting Silver layer...")
    tables = {
        'users': users_silver,
        'subscriptions': subscriptions_silver,
        'payments': payments_silver,
        'usage_logs': usage_logs_silver,
        'events': events_silver,
    }
    
    for table_name, df in tables.items():
        write_parquet_snapshot(df, silver_path, table_name, run_date)
        count = df.count()
        print(f"  {table_name}: {count:,} rows")
    
    print(f"\n✓ Silver layer created successfully at: {silver_path}")
