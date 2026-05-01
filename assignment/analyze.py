import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent
RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"


def main():
    customers = pd.read_csv(PROCESSED / "customers_clean.csv")
    orders = pd.read_csv(PROCESSED / "orders_clean.csv")
    products = pd.read_csv(RAW / "products.csv")

    df = pd.merge(orders, customers, on='customer_id', how='left')

    df = pd.merge(
        df,
        products,
        left_on='product',
        right_on='product_name',
        how='left'
    )


    monthly = (
        df[df['status'] == 'completed']
        .groupby('order_year_month')['amount']
        .sum()
        .reset_index()
    )

    monthly.to_csv(PROCESSED / "monthly_revenue.csv", index=False)

    top = (
        df[df['status'] == 'completed']
        .groupby(['customer_id', 'name', 'region'])['amount']
        .sum()
        .reset_index(name='total_spend')
        .sort_values('total_spend', ascending=False)
        .head(10)
    )

    top.to_csv(PROCESSED / "top_customers.csv", index=False)


if __name__ == "__main__":
    main()