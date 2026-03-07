"""Churn prediction model."""

import json
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from pyspark.sql import SparkSession

from ..common.io import read_parquet_snapshot


def train_churn_model(
    spark: SparkSession,
    gold_path: Path,
    run_date: str,
    output_path: Path,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Train churn prediction model.
    
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
    print(f"TRAINING CHURN MODEL")
    print(f"{'='*60}\n")
    
    # Load features and labels
    print("Loading data...")
    features_df = read_parquet_snapshot(spark, gold_path, 'ml_features', run_date)
    labels_df = read_parquet_snapshot(spark, gold_path, 'churn_labels', run_date)
    
    # Join features and labels
    ml_df = features_df.join(labels_df, 'user_id', 'inner')
    
    # Convert to pandas
    pdf = ml_df.toPandas()
    print(f"Total samples: {len(pdf):,}")
    print(f"Churn rate: {pdf['label'].mean():.2%}")
    
    # Define feature columns
    feature_cols = [
        'last_7d_minutes', 'last_7d_sessions',
        'last_30d_minutes', 'last_30d_sessions',
        'payment_fail_rate_30d',
        'tenure_days',
        'promo_exposure_30d',
        'outage_exposure_30d',
        'lifetime_minutes',
        'lifetime_sessions',
        'avg_daily_minutes',
        'days_active',
        'lifetime_revenue',
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
    y = pdf['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )
    
    print(f"\nTrain size: {len(X_train):,}")
    print(f"Test size: {len(X_test):,}")
    
    # Train model
    print("\nTraining Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=50,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    metrics = {
        'model': 'churn_classifier',
        'run_date': run_date,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred, zero_division=0)),
        'recall': float(recall_score(y_test, y_pred, zero_division=0)),
        'f1': float(f1_score(y_test, y_pred, zero_division=0)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
    }
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_,
    }).sort_values('importance', ascending=False)
    
    metrics['top_features'] = feature_importance.head(10).to_dict('records')
    
    # Save metrics
    output_path.mkdir(parents=True, exist_ok=True)
    metrics_file = output_path / f'churn_metrics_{run_date}.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n{'='*60}")
    print("CHURN MODEL METRICS")
    print(f"{'='*60}")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 Score:  {metrics['f1']:.4f}")
    print(f"ROC AUC:   {metrics['roc_auc']:.4f}")
    print(f"\nTop 5 Features:")
    for feat in feature_importance.head(5).itertuples():
        print(f"  {feat.feature}: {feat.importance:.4f}")
    
    print(f"\n✓ Metrics saved to: {metrics_file}")
    
    return metrics
