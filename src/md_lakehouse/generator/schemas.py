"""Data schemas for Bronze layer tables."""

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    DateType,
    TimestampType,
    BooleanType,
)


# Users table schema
USERS_SCHEMA = StructType([
    StructField("user_id", StringType(), nullable=False),
    StructField("signup_date", DateType(), nullable=False),
    StructField("age", IntegerType(), nullable=False),
    StructField("city", StringType(), nullable=False),
    StructField("acquisition_channel", StringType(), nullable=False),
])

# Subscriptions table schema
SUBSCRIPTIONS_SCHEMA = StructType([
    StructField("subscription_id", StringType(), nullable=False),
    StructField("user_id", StringType(), nullable=False),
    StructField("plan", StringType(), nullable=False),
    StructField("start_date", DateType(), nullable=False),
    StructField("end_date", DateType(), nullable=True),
    StructField("status", StringType(), nullable=False),  # active, cancelled, expired
])

# Payments table schema
PAYMENTS_SCHEMA = StructType([
    StructField("payment_id", StringType(), nullable=False),
    StructField("user_id", StringType(), nullable=False),
    StructField("ts", TimestampType(), nullable=False),
    StructField("amount", DoubleType(), nullable=False),
    StructField("method", StringType(), nullable=False),
    StructField("success", BooleanType(), nullable=False),
])

# Usage logs table schema
USAGE_LOGS_SCHEMA = StructType([
    StructField("log_id", StringType(), nullable=False),
    StructField("user_id", StringType(), nullable=False),
    StructField("ts", TimestampType(), nullable=False),
    StructField("sessions", IntegerType(), nullable=False),
    StructField("minutes", DoubleType(), nullable=False),
    StructField("feature_a", IntegerType(), nullable=False),
    StructField("feature_b", IntegerType(), nullable=False),
    StructField("feature_c", IntegerType(), nullable=False),
])

# Events table schema
EVENTS_SCHEMA = StructType([
    StructField("event_id", StringType(), nullable=False),
    StructField("date", DateType(), nullable=False),
    StructField("event_type", StringType(), nullable=False),  # promo, outage, price_change
    StructField("intensity", DoubleType(), nullable=False),
    StructField("affected_segment", StringType(), nullable=True),
])
