import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
from src.logging_setup import get_logger

logger = get_logger("charts")


def apply_theme(fig, ax, dark_mode: bool = False):
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    text_color = "#888888"
    ax.tick_params(colors=text_color, labelsize=14)
    ax.xaxis.label.set_color(text_color)
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_color(text_color)
    ax.yaxis.label.set_size(14)
    ax.title.set_color(text_color)
    ax.title.set_size(16)
    for spine in ax.spines.values():
        spine.set_edgecolor(text_color)
    return fig, ax


def plot_top_ips(grouped_df: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    if grouped_df.empty:
        return None

    top = grouped_df.head(top_n)

    fig, ax = plt.subplots(figsize=(14, 6))
    apply_theme(fig, ax)

    ax.barh(top["ip"], top["count"], color="steelblue")
    ax.set_xlabel("Request Count")
    ax.set_title(f"Top {top_n} IPs by Request Count")
    ax.invert_yaxis()

    plt.tight_layout()
    logger.info(f"Bar chart: top {top_n} IPs plotted")
    return fig


def plot_request_distribution(
    grouped_df: pd.DataFrame, dark_mode: bool = False
) -> plt.Figure:
    if grouped_df.empty:
        return None

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    apply_theme(fig, axes[0], dark_mode)
    apply_theme(fig, axes[1], dark_mode)

    axes[0].hist(grouped_df["count"], bins=20, color="steelblue", edgecolor="white")
    axes[0].set_title("Request Count Distribution")
    axes[0].set_xlabel("Requests")
    axes[0].set_ylabel("Number of IPs")

    sns.boxplot(y=grouped_df["count"], ax=axes[1], color="steelblue")
    axes[1].set_title("Box Plot — Requests per IP")
    axes[1].set_ylabel("Request Count")

    for ax in axes:
        ax.tick_params(labelsize=9)
        ax.xaxis.label.set_size(9)
        ax.yaxis.label.set_size(9)
        ax.title.set_size(12)

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
        color_continuous_scale="Viridis",
        title=f"Top {top_n} IPs — Interactive",
        labels={"count": "Requests", "ip": "IP Address"},
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis={"autorange": "reversed"},
        font=dict(size=16, color="gray"),
        title_font=dict(size=20, color="gray"),
        xaxis=dict(
            title_font=dict(size=13, color="gray"),
            tickfont=dict(size=15, color="gray"),
        ),
        yaxis_title="IP Address",
        yaxis_title_font=dict(size=13, color="gray"),
    )

    logger.info(f"Plotly chart: top {top_n} IPs")
    return fig
