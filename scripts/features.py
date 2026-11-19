"""Add duration_minutes and weekday feature columns."""

from pathlib import Path

import pandas as pd

IN = Path("data/transformed/events.csv")
OUT = Path("data/features/events.csv")


def main() -> None:
    df = pd.read_csv(IN)
    df["duration_minutes"] = df["duration_seconds"] / 60
    df["weekday"] = pd.to_datetime(df["date"]).dt.day_name()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"features: wrote {len(df)} rows to {OUT}")


if __name__ == "__main__":
    main()
