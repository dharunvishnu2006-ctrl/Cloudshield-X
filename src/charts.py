import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
from src.logging_setup import get_logger

logger = get_logger("charts")


def apply_theme(fig, ax):
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    return fig, ax


def plot_top_ips(grouped_df: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    if grouped_df.empty:
        return None

    top = grouped_df.head(top_n)

    fig, ax = plt.subplots(figsize=(10, 5))
    apply_theme(fig, ax)

    ax.barh(top["ip"], top["count"], color="steelblue")
    ax.set_xlabel("Request Count")
    ax.set_title(f"Top {top_n} IPs by Request Count")
    ax.invert_yaxis()

    plt.tight_layout()
    logger.info(f"Bar chart: top {top_n} IPs plotted")
    return fig


def plot_request_distribution(grouped_df: pd.DataFrame) -> plt.Figure:
    if grouped_df.empty:
        return None

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    apply_theme(fig, axes[0])
    apply_theme(fig, axes[1])

    axes[0].hist(grouped_df["count"], bins=20, color="steelblue", edgecolor="white")
    axes[0].set_title("Request Count Distribution")
    axes[0].set_xlabel("Requests")
    axes[0].set_ylabel("Number of IPs")

    sns.boxplot(y=grouped_df["count"], ax=axes[1], color="steelblue")
    axes[1].set_title("Box Plot — Requests per IP")
    axes[1].set_ylabel("Request Count")

    plt.tight_layout()
    logger.info("Distribution chart plotted")
    return fig


def plot_interactive_top_ips(grouped_df: pd.DataFrame, top_n: int = 10):
    if grouped_df.empty:
        return None

    top = grouped_df.head(top_n)

    fig = px.bar(
        top,
        x="count",
        y="ip",
        orientation="h",
        color="count",
        color_continuous_scale="Blues",
        title=f"Top {top_n} IPs — Interactive",
        labels={"count": "Requests", "ip": "IP Address"},
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis={"autorange": "reversed"},
    )

    logger.info(f"Plotly chart: top {top_n} IPs")
    return fig
