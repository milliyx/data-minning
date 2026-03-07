"""Report generation utilities."""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


def generate_evaluation_report(
    metrics: Dict[str, Any],
    output_path: Path,
    run_date: str,
) -> None:
    """
    Generate comprehensive evaluation report.
    
    Args:
        metrics: Dictionary with all model metrics
        output_path: Output path for report
        run_date: Run date
    """
    output_path.mkdir(parents=True, exist_ok=True)
    report_file = output_path / f'evaluation_report_{run_date}.md'
    
    with open(report_file, 'w') as f:
        f.write(f"# Model Evaluation Report\n\n")
        f.write(f"**Run Date:** {run_date}\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # Churn Model
        if 'churn' in metrics:
            churn = metrics['churn']
            f.write("## Churn Prediction Model\n\n")
            f.write(f"**Model Type:** Random Forest Classifier\n\n")
            f.write("### Performance Metrics\n\n")
            f.write(f"- **Accuracy:** {churn['accuracy']:.4f}\n")
            f.write(f"- **Precision:** {churn['precision']:.4f}\n")
            f.write(f"- **Recall:** {churn['recall']:.4f}\n")
            f.write(f"- **F1 Score:** {churn['f1']:.4f}\n")
            f.write(f"- **ROC AUC:** {churn['roc_auc']:.4f}\n\n")
            
            f.write("### Dataset\n\n")
            f.write(f"- **Training Samples:** {churn['train_samples']:,}\n")
            f.write(f"- **Test Samples:** {churn['test_samples']:,}\n\n")
            
            if 'top_features' in churn:
                f.write("### Top Features\n\n")
                f.write("| Feature | Importance |\n")
                f.write("|---------|------------|\n")
                for feat in churn['top_features'][:10]:
                    f.write(f"| {feat['feature']} | {feat['importance']:.4f} |\n")
                f.write("\n")
            
            f.write("---\n\n")
        
        # LTV Model
        if 'ltv' in metrics:
            ltv = metrics['ltv']
            f.write("## LTV Prediction Model\n\n")
            f.write(f"**Model Type:** Random Forest Regressor\n\n")
            f.write("### Performance Metrics\n\n")
            f.write(f"- **MAE:** ${ltv['mae']:.2f}\n")
            f.write(f"- **RMSE:** ${ltv['rmse']:.2f}\n")
            f.write(f"- **R² Score:** {ltv['r2']:.4f}\n")
            f.write(f"- **Mean Actual LTV:** ${ltv['mean_actual']:.2f}\n")
            f.write(f"- **Mean Predicted LTV:** ${ltv['mean_predicted']:.2f}\n\n")
            
            f.write("### Dataset\n\n")
            f.write(f"- **Training Samples:** {ltv['train_samples']:,}\n")
            f.write(f"- **Test Samples:** {ltv['test_samples']:,}\n\n")
            
            if 'top_features' in ltv:
                f.write("### Top Features\n\n")
                f.write("| Feature | Importance |\n")
                f.write("|---------|------------|\n")
                for feat in ltv['top_features'][:10]:
                    f.write(f"| {feat['feature']} | {feat['importance']:.4f} |\n")
                f.write("\n")
            
            f.write("---\n\n")
        
        # Segmentation Model
        if 'segmentation' in metrics:
            seg = metrics['segmentation']
            f.write("## User Segmentation Model\n\n")
            f.write(f"**Model Type:** K-Means Clustering\n\n")
            f.write("### Performance Metrics\n\n")
            f.write(f"- **Number of Clusters:** {seg['n_clusters']}\n")
            f.write(f"- **Silhouette Score:** {seg['silhouette_score']:.4f}\n")
            f.write(f"- **Calinski-Harabasz Score:** {seg['calinski_harabasz_score']:.2f}\n\n")
            
            f.write("### Segment Profiles\n\n")
            f.write("| Segment | Size | % | Avg Revenue | Avg Engagement | Avg Tenure |\n")
            f.write("|---------|------|---|-------------|----------------|------------|\n")
            for profile in seg['segments']:
                name = profile.get('segment_name', f"Segment {profile['segment_id']}")
                f.write(
                    f"| {name} | {profile['size']:,} | "
                    f"{profile['percentage']:.1f}% | "
                    f"${profile['avg_revenue']:.2f} | "
                    f"{profile['avg_engagement']:.2f} | "
                    f"{profile['avg_tenure']:.0f} days |\n"
                )
            f.write("\n")
        
        f.write("---\n\n")
        f.write("## Summary\n\n")
        f.write("All models have been trained and evaluated successfully. ")
        f.write("Review the metrics above to assess model performance.\n\n")
        f.write("### Recommendations\n\n")
        f.write("1. Monitor model performance over time\n")
        f.write("2. Retrain models with new data regularly\n")
        f.write("3. Investigate low-performing segments\n")
        f.write("4. Use churn predictions for targeted interventions\n")
        f.write("5. Leverage LTV predictions for customer prioritization\n")
    
    print(f"\n✓ Evaluation report generated: {report_file}")


def print_summary(metrics: Dict[str, Any]) -> None:
    """
    Print a summary of all model metrics.
    
    Args:
        metrics: Dictionary with all model metrics
    """
    print(f"\n{'='*60}")
    print("MODEL EVALUATION SUMMARY")
    print(f"{'='*60}\n")
    
    if 'churn' in metrics:
        print("Churn Model:")
        print(f"  F1 Score: {metrics['churn']['f1']:.4f}")
        print(f"  ROC AUC:  {metrics['churn']['roc_auc']:.4f}\n")
    
    if 'ltv' in metrics:
        print("LTV Model:")
        print(f"  R² Score: {metrics['ltv']['r2']:.4f}")
        print(f"  MAE:      ${metrics['ltv']['mae']:.2f}\n")
    
    if 'segmentation' in metrics:
        print("Segmentation Model:")
        print(f"  Silhouette Score: {metrics['segmentation']['silhouette_score']:.4f}")
        print(f"  N Segments:       {metrics['segmentation']['n_clusters']}\n")
