"""Simple data generator script for bronze table parquet files."""
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_data(num_rows: int = 1000, start_date: str = None):
    """Generate a DataFrame with sales data for bronze table."""
    if start_date is None:
        start = datetime.now() - timedelta(days=365)
    else:
        start = datetime.fromisoformat(start_date)

    # Generate timestamps
    dates = [start + timedelta(days=i) for i in range(num_rows // 10)] * 10
    random.shuffle(dates)
    dates = sorted(dates[:num_rows])

    # Generate customer IDs
    customer_ids = [f"CUST_{random.randint(1000, 9999)}" for _ in range(num_rows)]

    # Generate product categories
    categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
    products = [random.choice(categories) for _ in range(num_rows)]

    # Generate sales amounts
    amounts = np.random.exponential(100, num_rows).round(2)

    # Generate quantities
    quantities = np.random.poisson(2, num_rows) + 1

    # Generate payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'PayPal']
    payments = [random.choice(payment_methods) for _ in range(num_rows)]

    df = pd.DataFrame({
        "transaction_id": range(1, num_rows + 1),
        "timestamp": dates,
        "customer_id": customer_ids,
        "product_category": products,
        "sales_amount": amounts,
        "quantity": quantities,
        "payment_method": payments,
    })
    return df


def save_parquet(df: pd.DataFrame, path: str):
    """Save DataFrame to Parquet, creating directories if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)


def main():
    df = generate_data(5000)
    save_parquet(df, "data/bronze/sales_data.parquet")
    print(f"Wrote {len(df)} rows to data/bronze/sales_data.parquet")


if __name__ == "__main__":
    main()
