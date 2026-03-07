"""Metrics computation utilities."""

import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd


def load_metrics(metrics_path: Path, run_date: str) -> Dict[str, Any]:
    """
    Load all model metrics for a given run date.
    
    Args:
        metrics_path: Path to metrics directory
        run_date: Run date
        
    Returns:
        Dictionary with all model metrics
    """
    all_metrics = {}
    
    # Load churn metrics
    churn_file = metrics_path / f'churn_metrics_{run_date}.json'
    if churn_file.exists():
        with open(churn_file) as f:
            all_metrics['churn'] = json.load(f)
    
    # Load LTV metrics
    ltv_file = metrics_path / f'ltv_metrics_{run_date}.json'
    if ltv_file.exists():
        with open(ltv_file) as f:
            all_metrics['ltv'] = json.load(f)
    
    # Load segmentation metrics
    seg_file = metrics_path / f'segmentation_metrics_{run_date}.json'
    if seg_file.exists():
        with open(seg_file) as f:
            all_metrics['segmentation'] = json.load(f)
    
    return all_metrics


def compare_metrics(
    metrics_path: Path,
    run_dates: List[str],
) -> pd.DataFrame:
    """
    Compare metrics across multiple run dates.
    
    Args:
        metrics_path: Path to metrics directory
        run_dates: List of run dates to compare
        
    Returns:
        DataFrame with metrics comparison
    """
    comparison_data = []
    
    for run_date in run_dates:
        metrics = load_metrics(metrics_path, run_date)
        
        row = {'run_date': run_date}
        
        if 'churn' in metrics:
            row['churn_f1'] = metrics['churn']['f1']
            row['churn_roc_auc'] = metrics['churn']['roc_auc']
        
        if 'ltv' in metrics:
            row['ltv_r2'] = metrics['ltv']['r2']
            row['ltv_mae'] = metrics['ltv']['mae']
        
        if 'segmentation' in metrics:
            row['seg_silhouette'] = metrics['segmentation']['silhouette_score']
        
        comparison_data.append(row)
    
    return pd.DataFrame(comparison_data)
