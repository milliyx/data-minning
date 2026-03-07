"""Command-line interface for MD Lakehouse."""

import click
from pathlib import Path
import sys

from .common.spark import get_spark_session, stop_spark_session
from .common.config import load_team_config
from .generator.generate import generate_bronze_data
from .pipelines.bronze_to_silver import bronze_to_silver_pipeline
from .pipelines.silver_to_gold import silver_to_gold_pipeline
from .features.build_features import build_ml_features
from .models.churn import train_churn_model
from .models.ltv import train_ltv_model
from .models.segmentation import train_segmentation_model
from .evaluation.metrics import load_metrics
from .evaluation.reports import generate_evaluation_report, print_summary


@click.group()
def cli():
    """MD Lakehouse - Local Lakehouse for Data Mining Course."""
    pass


@cli.command()
@click.option('--team', required=True, type=click.Path(exists=True), help='Team config file path')
@click.option('--run-date', required=True, help='Run date (YYYY-MM-DD)')
def generate(team: str, run_date: str):
    """Generate Bronze layer data."""
    team_path = Path(team)
    base_path = Path(__file__).parent.parent.parent / 'configs' / 'base.yaml'
    
    # Load config
    config = load_team_config(team_path, base_path)
    team_id = config.get('team_id', 'unknown')
    seed = config.get('seed', 42)
    
    # Override with CI settings if enabled
    if config.get('ci_mode', False):
        config['simulation']['population_size'] = config['ci_population']
        config['simulation']['months_history'] = config['ci_months']
    
    # Get spark session
    spark = get_spark_session(
        app_name=config['spark']['app_name'],
        master=config['spark']['master'],
        memory=config['spark']['memory'],
    )
    
    try:
        output_base = Path(config['data']['base_path'])
        generate_bronze_data(spark, config, team_id, seed, run_date, output_base)
    finally:
        stop_spark_session(spark)


@cli.command()
@click.option('--team', required=True, type=click.Path(exists=True), help='Team config file path')
@click.option('--run-date', required=True, help='Run date (YYYY-MM-DD)')
def pipeline(team: str, run_date: str):
    """Run ETL pipeline (Bronze → Silver → Gold)."""
    team_path = Path(team)
    base_path = Path(__file__).parent.parent.parent / 'configs' / 'base.yaml'
    
    # Load config
    config = load_team_config(team_path, base_path)
    
    # Get spark session
    spark = get_spark_session(
        app_name=config['spark']['app_name'],
        master=config['spark']['master'],
        memory=config['spark']['memory'],
    )
    
    try:
        data_base = Path(config['data']['base_path'])
        bronze_path = data_base / 'bronze'
        silver_path = data_base / 'silver'
        gold_path = data_base / 'gold'
        
        # Bronze → Silver
        bronze_to_silver_pipeline(spark, bronze_path, silver_path, run_date)
        
        # Silver → Gold
        silver_to_gold_pipeline(spark, silver_path, gold_path, run_date)
        
    finally:
        stop_spark_session(spark)


@cli.command()
@click.option('--team', required=True, type=click.Path(exists=True), help='Team config file path')
@click.option('--run-date', required=True, help='Run date (YYYY-MM-DD)')
def features(team: str, run_date: str):
    """Build ML features."""
    team_path = Path(team)
    base_path = Path(__file__).parent.parent.parent / 'configs' / 'base.yaml'
    
    # Load config
    config = load_team_config(team_path, base_path)
    
    # Get spark session
    spark = get_spark_session(
        app_name=config['spark']['app_name'],
        master=config['spark']['master'],
        memory=config['spark']['memory'],
    )
    
    try:
        gold_path = Path(config['data']['base_path']) / 'gold'
        build_ml_features(spark, gold_path, run_date)
    finally:
        stop_spark_session(spark)


@cli.command()
@click.option('--team', required=True, type=click.Path(exists=True), help='Team config file path')
@click.option('--run-date', required=True, help='Run date (YYYY-MM-DD)')
def train(team: str, run_date: str):
    """Train all ML models."""
    team_path = Path(team)
    base_path = Path(__file__).parent.parent.parent / 'configs' / 'base.yaml'
    
    # Load config
    config = load_team_config(team_path, base_path)
    seed = config.get('seed', 42)
    
    # Get spark session
    spark = get_spark_session(
        app_name=config['spark']['app_name'],
        master=config['spark']['master'],
        memory=config['spark']['memory'],
    )
    
    try:
        gold_path = Path(config['data']['base_path']) / 'gold'
        output_path = Path('data') / 'models'
        
        # Train churn model
        train_churn_model(spark, gold_path, run_date, output_path, random_state=seed)
        
        # Train LTV model
        train_ltv_model(spark, gold_path, run_date, output_path, random_state=seed)
        
        # Train segmentation model
        train_segmentation_model(spark, gold_path, run_date, output_path, random_state=seed)
        
    finally:
        stop_spark_session(spark)


@cli.command()
@click.option('--team', required=True, type=click.Path(exists=True), help='Team config file path')
@click.option('--run-date', required=True, help='Run date (YYYY-MM-DD)')
def evaluate(team: str, run_date: str):
    """Generate evaluation reports."""
    team_path = Path(team)
    base_path = Path(__file__).parent.parent.parent / 'configs' / 'base.yaml'
    
    # Load config
    config = load_team_config(team_path, base_path)
    
    metrics_path = Path('data') / 'models'
    output_path = Path('data') / 'reports'
    
    # Load metrics
    metrics = load_metrics(metrics_path, run_date)
    
    if not metrics:
        print("No metrics found. Please run 'train' first.")
        sys.exit(1)
    
    # Generate report
    generate_evaluation_report(metrics, output_path, run_date)
    
    # Print summary
    print_summary(metrics)


@cli.command()
@click.option('--team', required=True, type=click.Path(exists=True), help='Team config file path')
@click.option('--run-date', required=True, help='Run date (YYYY-MM-DD)')
def all(team: str, run_date: str):
    """Run complete pipeline: generate → pipeline → features → train → evaluate."""
    click.echo(f"\n{'='*60}")
    click.echo("RUNNING COMPLETE PIPELINE")
    click.echo(f"Team: {team}")
    click.echo(f"Run Date: {run_date}")
    click.echo(f"{'='*60}\n")
    
    # Run all steps in sequence
    ctx = click.get_current_context()
    
    click.echo("\n[1/5] Generating Bronze data...")
    ctx.invoke(generate, team=team, run_date=run_date)
    
    click.echo("\n[2/5] Running ETL pipeline...")
    ctx.invoke(pipeline, team=team, run_date=run_date)
    
    click.echo("\n[3/5] Building features...")
    ctx.invoke(features, team=team, run_date=run_date)
    
    click.echo("\n[4/5] Training models...")
    ctx.invoke(train, team=team, run_date=run_date)
    
    click.echo("\n[5/5] Generating evaluation reports...")
    ctx.invoke(evaluate, team=team, run_date=run_date)
    
    click.echo(f"\n{'='*60}")
    click.echo("✓ COMPLETE PIPELINE FINISHED SUCCESSFULLY")
    click.echo(f"{'='*60}\n")


if __name__ == '__main__':
    cli()
