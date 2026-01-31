import pandas as pd


# -----------------------------
# Helper: parse API response
# -----------------------------
def parse_earnings_response(response: dict) -> pd.DataFrame:
    records = []

    for symbol, payload in response["data"].items():
        for row in payload["data"]:
            records.append(
                {
                    "symbol": symbol,
                    "date": row["date"],
                    "event_return": row["event_return"],
                    "pre_return": row["pre_return"],
                    "post_return": row["post_return"],
                    "volatility_pre": row["volatility_pre"],
                    "volatility_post": row["volatility_post"],
                    "gap": row["gap"],
                },
            )

    df = pd.DataFrame(records)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    return df
