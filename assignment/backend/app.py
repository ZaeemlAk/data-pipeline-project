from fastapi import FastAPI, HTTPException
import pandas as pd
from pathlib import Path

app = FastAPI()
DATA = Path(__file__).parent.parent / "data" / "processed"


def read_csv(name):
    path = DATA / name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Not found")
    return pd.read_csv(path).to_dict(orient="records")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/revenue")
def revenue():
    return read_csv("monthly_revenue.csv")