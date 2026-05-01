import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

BASE = Path(__file__).parent
RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"


def parse_date(val):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except:
            pass
    return pd.NaT


def load_csv(path):
    return pd.read_csv(path)


def clean_customers(df):
    df['name'] = df['name'].str.strip()
    df['region'] = df['region'].str.strip()
    df['email'] = df['email'].str.lower()

    df['is_valid_email'] = df['email'].apply(
        lambda x: isinstance(x, str) and '@' in x and '.' in x
    )

    df['signup_date'] = df['signup_date'].apply(parse_date)

    df = df.sort_values('signup_date').drop_duplicates(
        'customer_id', keep='last'
    )

    df['region'] = df['region'].fillna("Unknown")

    return df


def clean_orders(df):
    df['order_date'] = df['order_date'].apply(parse_date)

    df = df.dropna(subset=['customer_id', 'order_id'], how='all')

    df['amount'] = df.groupby('product')['amount'].transform(
        lambda x: x.fillna(x.median())
    )

    status_map = {
        'done': 'completed',
        'completed': 'completed',
        'pending': 'pending',
        'canceled': 'cancelled',
        'cancelled': 'cancelled',
        'refunded': 'refunded'
    }

    df['status'] = df['status'].str.lower().map(status_map)

    df['order_year_month'] = df['order_date'].dt.strftime('%Y-%m')

    return df


def main():
    customers = load_csv(RAW / "customers.csv")
    orders = load_csv(RAW / "orders.csv")

    PROCESSED.mkdir(parents=True, exist_ok=True)

    clean_customers(customers).to_csv(PROCESSED / "customers_clean.csv", index=False)
    clean_orders(orders).to_csv(PROCESSED / "orders_clean.csv", index=False)


if __name__ == "__main__":
    main()