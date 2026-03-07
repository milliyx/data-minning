"""Feature engineering for ML models."""

from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F

from ..common.io import read_parquet_snapshot, write_parquet_snapshot


def build_ml_features(
    spark: SparkSession,
    gold_path: Path,
    run_date: str,
) -> None:
    """
    Build comprehensive ML features from Gold layer.
    
    This combines churn features with additional derived features
    for all ML models (churn, LTV, segmentation).
    
    Args:
        spark: SparkSession
        gold_path: Gold layer base path
        run_date: Run date in YYYY-MM-DD format
    """
    print(f"\n{'='*60}")
    print(f"FEATURE ENGINEERING")
    print(f"Run Date: {run_date}")
    print(f"{'='*60}\n")
    
    # Read Gold tables
    print("Reading Gold layer...")
    churn_features = read_parquet_snapshot(spark, gold_path, 'churn_features', run_date)
    fact_usage = read_parquet_snapshot(spark, gold_path, 'fact_usage_daily', run_date)
    fact_revenue = read_parquet_snapshot(spark, gold_path, 'fact_revenue_daily', run_date)
    
    # Calculate lifetime metrics
    print("Computing lifetime metrics...")
    lifetime_usage = (
        fact_usage
        .groupBy('user_id')
        .agg(
            F.sum('minutes').alias('lifetime_minutes'),
            F.sum('sessions').alias('lifetime_sessions'),
            F.avg('minutes').alias('avg_daily_minutes'),
            F.count('*').alias('days_active'),
        )
    )
    
    lifetime_revenue = (
        fact_revenue
        .groupBy('user_id')
        .agg(
            F.sum('revenue').alias('lifetime_revenue'),
            F.sum('payment_failures').alias('lifetime_payment_failures'),
            F.avg('revenue').alias('avg_payment'),
        )
    )
    
    # Combine into comprehensive feature table
    print("Building comprehensive feature table...")
    ml_features = (
        churn_features
        .join(lifetime_usage, 'user_id', 'left')
        .join(lifetime_revenue, 'user_id', 'left')
        .fillna(0)
        # Add derived features
        .withColumn(
            'usage_trend',
            F.when(F.col('last_30d_minutes') > 0, 
                   F.col('last_7d_minutes') / (F.col('last_30d_minutes') / 4.0)
            ).otherwise(0)
        )
        .withColumn(
            'engagement_score',
            (F.col('last_30d_minutes') / 30.0) / 
            F.when(F.col('plan') == 'premium', 120)
             .when(F.col('plan') == 'standard', 60)
             .otherwise(30)
        )
        .withColumn(
            'payment_health',
            1 - F.col('payment_fail_rate_30d')
        )
    )
    
    # Write ML features
    write_parquet_snapshot(ml_features, gold_path, 'ml_features', run_date)
    count = ml_features.count()
    print(f"\n✓ ML features table created: {count:,} rows")
    print(f"  Columns: {len(ml_features.columns)}")
    print(f"  Feature columns: {ml_features.columns}")
