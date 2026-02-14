"""Spark session management."""

from pyspark.sql import SparkSession
from typing import Optional


def get_spark_session(
    app_name: str = "MD-Lakehouse",
    master: str = "local[*]",
    memory: str = "2g",
    additional_config: Optional[dict] = None,
) -> SparkSession:
    """
    Create or get existing Spark session with sensible defaults.
    
    Args:
        app_name: Application name
        master: Spark master URL
        memory: Driver memory allocation
        additional_config: Additional Spark configuration options
        
    Returns:
        Configured SparkSession
    """
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.driver.memory", memory)
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.default.parallelism", "8")
        # Suppress verbose logging
        .config("spark.ui.showConsoleProgress", "false")
    )
    
    if additional_config:
        for key, value in additional_config.items():
            builder = builder.config(key, value)
    
    spark = builder.getOrCreate()
    
    # Set log level to reduce noise
    spark.sparkContext.setLogLevel("WARN")
    
    return spark


def stop_spark_session(spark: SparkSession) -> None:
    """
    Stop the Spark session.
    
    Args:
        spark: SparkSession to stop
    """
    if spark:
        spark.stop()
