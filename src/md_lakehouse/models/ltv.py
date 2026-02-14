"""LTV (Lifetime Value) regression model."""

import json
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from pyspark.sql import SparkSession

from ..common.io import read_parquet_snapshot


def train_ltv_model(
    spark: SparkSession,
    gold_path: Path,
    run_date: str,
    output_path: Path,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Train LTV prediction model.
    
    Predicts future revenue based on current engagement and behavior.
    
    Args:
        spark: SparkSession
        gold_path: Gold layer base path
        run_date: Run date
        output_path: Output path for model artifacts
        random_state: Random state for reproducibility
        
    Returns:
        Dictionary with model metrics
    """
    print(f"\n{'='*60}")
    print(f"TRAINING LTV MODEL")
    print(f"{'='*60}\n")
    
    # Load features
    print("Loading data...")
    features_df = read_parquet_snapshot(spark, gold_path, 'ml_features', run_date)
    
    # Convert to pandas
    pdf = features_df.toPandas()
    
    # Target: lifetime_revenue (actual LTV so far)
    # In production, this would be predicted future revenue
    # For this course, we use actual LTV as proxy
    pdf = pdf[pdf['lifetime_revenue'] > 0].copy()
    
    print(f"Total samples: {len(pdf):,}")
    print(f"Average LTV: ${pdf['lifetime_revenue'].mean():.2f}")
    print(f"Median LTV: ${pdf['lifetime_revenue'].median():.2f}")
    
    # Define feature columns
    feature_cols = [
        'last_7d_minutes', 'last_7d_sessions',
        'last_30d_minutes', 'last_30d_sessions',
        'payment_fail_rate_30d',
        'tenure_days',
        'promo_exposure_30d',
        'outage_exposure_30d',
        'lifetime_sessions',
        'avg_daily_minutes',
        'days_active',
        'lifetime_payment_failures',
        'avg_payment',
        'usage_trend',
        'engagement_score',
        'payment_health',
    ]
    
    # One-hot encode plan
    plan_dummies = pd.get_dummies(pdf['plan'], prefix='plan')
    X_features = pdf[feature_cols].copy()
    X = pd.concat([X_features, plan_dummies], axis=1)
    y = pdf['lifetime_revenue']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )
    
    print(f"\nTrain size: {len(X_train):,}")
    print(f"Test size: {len(X_test):,}")
    
    # Train model
    print("\nTraining Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=50,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'model': 'ltv_regressor',
        'run_date': run_date,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'mae': float(mae),
        'rmse': float(rmse),
        'r2': float(r2),
        'mean_actual': float(y_test.mean()),
        'mean_predicted': float(y_pred.mean()),
    }
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_,
    }).sort_values('importance', ascending=False)
    
    metrics['top_features'] = feature_importance.head(10).to_dict('records')
    
    # Save metrics
    output_path.mkdir(parents=True, exist_ok=True)
    metrics_file = output_path / f'ltv_metrics_{run_date}.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n{'='*60}")
    print("LTV MODEL METRICS")
    print(f"{'='*60}")
    print(f"MAE:  ${metrics['mae']:.2f}")
    print(f"RMSE: ${metrics['rmse']:.2f}")
    print(f"R²:   {metrics['r2']:.4f}")
    print(f"\nMean Actual LTV:    ${metrics['mean_actual']:.2f}")
    print(f"Mean Predicted LTV: ${metrics['mean_predicted']:.2f}")
    print(f"\nTop 5 Features:")
    for feat in feature_importance.head(5).itertuples():
        print(f"  {feat.feature}: {feat.importance:.4f}")
    
    print(f"\n✓ Metrics saved to: {metrics_file}")
    
    return metrics
