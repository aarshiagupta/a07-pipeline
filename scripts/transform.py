"""Add a YYYY-MM-DD date column derived from the timestamp."""

from pathlib import Path

import pandas as pd

IN = Path("data/clean/events.csv")
OUT = Path("data/transformed/events.csv")


def main() -> None:
    df = pd.read_csv(IN)
    df["date"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"transform: wrote {len(df)} rows to {OUT}")


if __name__ == "__main__":
    main()
