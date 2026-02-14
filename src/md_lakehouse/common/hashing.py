"""Hashing utilities for reproducibility verification."""

import hashlib
from pyspark.sql import DataFrame
from typing import List


def compute_dataframe_hash(df: DataFrame, key_columns: List[str], sample_size: int = 1000) -> str:
    """
    Compute a stable hash of a DataFrame for reproducibility testing.
    
    Sorts by key columns, takes a sample, and computes hash of the CSV representation.
    This allows verifying that the same seed produces identical data.
    
    Args:
        df: DataFrame to hash
        key_columns: Columns to use for sorting
        sample_size: Number of rows to include in hash
        
    Returns:
        Hexadecimal hash string
    """
    # Sort by key columns for stability
    sorted_df = df.orderBy(*key_columns)
    
    # Take sample
    sample_df = sorted_df.limit(sample_size)
    
    # Convert to pandas and then to CSV string (deterministic)
    pandas_df = sample_df.toPandas()
    csv_string = pandas_df.to_csv(index=False, header=True)
    
    # Compute hash
    hash_obj = hashlib.sha256(csv_string.encode('utf-8'))
    return hash_obj.hexdigest()


def compute_row_count(df: DataFrame) -> int:
    """
    Compute row count of DataFrame.
    
    Args:
        df: DataFrame to count
        
    Returns:
        Number of rows
    """
    return df.count()
