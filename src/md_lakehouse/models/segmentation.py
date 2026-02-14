"""User segmentation clustering model."""

import json
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

from ..common.io import read_parquet_snapshot, write_parquet_snapshot


def train_segmentation_model(
    spark: SparkSession,
    gold_path: Path,
    run_date: str,
    output_path: Path,
    n_clusters: int = 4,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Train user segmentation clustering model.
    
    Args:
        spark: SparkSession
        gold_path: Gold layer base path
        run_date: Run date
        output_path: Output path for model artifacts
        n_clusters: Number of customer segments
        random_state: Random state for reproducibility
        
    Returns:
        Dictionary with model metrics
    """
    print(f"\n{'='*60}")
    print(f"TRAINING SEGMENTATION MODEL")
    print(f"{'='*60}\n")
    
    # Load features
    print("Loading data...")
    features_df = read_parquet_snapshot(spark, gold_path, 'ml_features', run_date)
    
    # Convert to pandas
    pdf = features_df.toPandas()
    print(f"Total users: {len(pdf):,}")
    
    # Define feature columns for segmentation
    feature_cols = [
        'last_30d_minutes',
        'last_30d_sessions',
        'tenure_days',
        'lifetime_revenue',
        'engagement_score',
        'payment_health',
    ]
    
    # Prepare features
    X = pdf[feature_cols].copy()
    user_ids = pdf['user_id'].copy()
    
    # Handle missing values
    X = X.fillna(0)
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train clustering model
    print(f"\nTraining K-Means with {n_clusters} clusters...")
    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10,
        max_iter=300,
    )
    clusters = model.fit_predict(X_scaled)
    
    # Calculate metrics
    silhouette = silhouette_score(X_scaled, clusters)
    calinski = calinski_harabasz_score(X_scaled, clusters)
    
    # Add clusters to dataframe
    pdf['segment_id'] = clusters
    
    # Analyze segments
    segment_profiles = []
    for i in range(n_clusters):
        segment_data = pdf[pdf['segment_id'] == i]
        profile = {
            'segment_id': int(i),
            'size': int(len(segment_data)),
            'percentage': float(len(segment_data) / len(pdf) * 100),
            'avg_revenue': float(segment_data['lifetime_revenue'].mean()),
            'avg_engagement': float(segment_data['engagement_score'].mean()),
            'avg_tenure': float(segment_data['tenure_days'].mean()),
            'avg_usage_30d': float(segment_data['last_30d_minutes'].mean()),
        }
        segment_profiles.append(profile)
    
    # Sort by revenue (descending)
    segment_profiles = sorted(segment_profiles, key=lambda x: x['avg_revenue'], reverse=True)
    
    # Assign meaningful names based on characteristics
    segment_names = ['VIP', 'Engaged', 'At-Risk', 'Inactive']
    for i, profile in enumerate(segment_profiles):
        if i < len(segment_names):
            profile['segment_name'] = segment_names[i]
        else:
            profile['segment_name'] = f'Segment_{i}'
    
    metrics = {
        'model': 'user_segmentation',
        'run_date': run_date,
        'n_clusters': n_clusters,
        'total_users': len(pdf),
        'silhouette_score': float(silhouette),
        'calinski_harabasz_score': float(calinski),
        'segments': segment_profiles,
    }
    
    # Save metrics
    output_path.mkdir(parents=True, exist_ok=True)
    metrics_file = output_path / f'segmentation_metrics_{run_date}.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n{'='*60}")
    print("SEGMENTATION MODEL METRICS")
    print(f"{'='*60}")
    print(f"Silhouette Score:      {metrics['silhouette_score']:.4f}")
    print(f"Calinski-Harabasz:     {metrics['calinski_harabasz_score']:.2f}")
    print(f"\nSegment Profiles:")
    for profile in segment_profiles:
        print(f"\n  {profile['segment_name']} (Segment {profile['segment_id']}):")
        print(f"    Size: {profile['size']:,} ({profile['percentage']:.1f}%)")
        print(f"    Avg Revenue: ${profile['avg_revenue']:.2f}")
        print(f"    Avg Engagement: {profile['avg_engagement']:.2f}")
        print(f"    Avg Tenure: {profile['avg_tenure']:.0f} days")
    
    # Save segment assignments to Gold layer
    print("\nSaving segment assignments...")
    segments_df = spark.createDataFrame(
        pdf[['user_id', 'segment_id']].assign(as_of_date=run_date)
    )
    write_parquet_snapshot(segments_df, gold_path, 'customer_segments', run_date)
    
    print(f"\n✓ Metrics saved to: {metrics_file}")
    print(f"✓ Segment assignments saved to Gold layer")
    
    return metrics
