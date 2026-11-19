"""Clean raw events: drop bad rows and normalize timestamps to ISO 8601."""

from pathlib import Path

import pandas as pd

RAW = Path("data/raw/events.csv")
OUT = Path("data/clean/events.csv")

VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}

# Timestamp formats observed in the raw data.
TIMESTAMP_FORMATS = [
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
]


def parse_timestamp(series: pd.Series) -> pd.Series:
    """Try each known format; return NaT where none match."""
    parsed = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")
    for fmt in TIMESTAMP_FORMATS:
        attempt = pd.to_datetime(series, format=fmt, errors="coerce")
        parsed = parsed.fillna(attempt)
    return parsed


def main() -> None:
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    df = df.apply(lambda col: col.str.strip())

    # Drop rows with any missing field.
    df = df[(df != "").all(axis=1)]

    # Drop invalid event types.
    df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

    # Drop non-numeric or non-positive durations.
    duration = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df[duration > 0].copy()
    df["duration_seconds"] = duration[duration > 0].astype(int)

    # Normalize timestamps; drop any that can't be parsed.
    ts = parse_timestamp(df["timestamp"])
    df = df[ts.notna()].copy()
    df["timestamp"] = ts[ts.notna()].dt.strftime("%Y-%m-%dT%H:%M:%S")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"clean: wrote {len(df)} rows to {OUT}")


if __name__ == "__main__":
    main()
