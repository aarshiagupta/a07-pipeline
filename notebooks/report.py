import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    from pathlib import Path

    return Path, mo, pd, plt


@app.cell
def _(mo):
    mo.md("""
    # Event Duration Report

    Distribution of event durations from the DVC pipeline output
    (`data/features/events.csv`).
    """)
    return


@app.cell
def _(Path, pd):
    data_path = Path(__file__).parent.parent / "data" / "features" / "events.csv"
    df = pd.read_csv(data_path)
    df.head()
    return (df,)


@app.cell
def _(df, plt):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(df["duration_minutes"], bins=30, color="#4C72B0", edgecolor="white")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of events")
    ax.set_title(f"Distribution of event durations (n={len(df)})")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    ax
    return


if __name__ == "__main__":
    app.run()
