"""I/O utilities for reading and writing data."""

from pathlib import Path
from pyspark.sql import DataFrame, SparkSession
from typing import Optional


def write_parquet_snapshot(
    df: DataFrame,
    base_path: Path,
    table_name: str,
    run_date: str,
    partition_cols: Optional[list] = None,
) -> Path:
    """
    Write DataFrame as Parquet snapshot with run_date partition.
    
    Args:
        df: DataFrame to write
        base_path: Base data directory path
        table_name: Name of the table
        run_date: Run date in YYYY-MM-DD format
        partition_cols: Additional partition columns (run_date is always added)
        
    Returns:
        Path where data was written
    """
    output_path = base_path / table_name / f"run_date={run_date}"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if partition_cols:
        df.write.partitionBy(*partition_cols).mode("overwrite").parquet(str(output_path))
    else:
        df.write.mode("overwrite").parquet(str(output_path))
    
    return output_path


def read_parquet_snapshot(
    spark: SparkSession,
    base_path: Path,
    table_name: str,
    run_date: str,
) -> DataFrame:
    """
    Read Parquet snapshot for specific run_date.
    
    Args:
        spark: SparkSession
        base_path: Base data directory path
        table_name: Name of the table
        run_date: Run date in YYYY-MM-DD format
        
    Returns:
        DataFrame with snapshot data
    """
    snapshot_path = base_path / table_name / f"run_date={run_date}"
    
    if not snapshot_path.exists():
        raise FileNotFoundError(f"Snapshot not found: {snapshot_path}")
    
    return spark.read.parquet(str(snapshot_path))


def read_latest_snapshot(
    spark: SparkSession,
    base_path: Path,
    table_name: str,
) -> DataFrame:
    """
    Read the latest snapshot of a table by scanning all run_date partitions.
    
    Args:
        spark: SparkSession
        base_path: Base data directory path
        table_name: Name of the table
        
    Returns:
        DataFrame with latest snapshot data
    """
    table_path = base_path / table_name
    
    if not table_path.exists():
        raise FileNotFoundError(f"Table directory not found: {table_path}")
    
    # Find all run_date partitions
    run_dates = sorted([
        d.name.replace("run_date=", "")
        for d in table_path.iterdir()
        if d.is_dir() and d.name.startswith("run_date=")
    ])
    
    if not run_dates:
        raise ValueError(f"No snapshots found for table: {table_name}")
    
    latest_date = run_dates[-1]
    return read_parquet_snapshot(spark, base_path, table_name, latest_date)


def table_exists(base_path: Path, table_name: str, run_date: str) -> bool:
    """
    Check if a table snapshot exists.
    
    Args:
        base_path: Base data directory path
        table_name: Name of the table
        run_date: Run date in YYYY-MM-DD format
        
    Returns:
        True if snapshot exists
    """
    snapshot_path = base_path / table_name / f"run_date={run_date}"
    return snapshot_path.exists()
