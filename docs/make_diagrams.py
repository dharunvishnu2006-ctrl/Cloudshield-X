import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

ROOT = Path(__file__).parent.parent
VERSIONS_FILE = ROOT / "docs" / "versions.json"
OUT_DIR = ROOT / "docs"


def load_versions() -> list[dict]:
    with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["versions"]


def make_architecture():
    fig, ax = plt.subplots(figsize=(14, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.axis("off")

    stages = [
        "Log File",
        "Reader\n(generator)",
        "Parser\n(regex)",
        "Validator\n(Pydantic)",
        "Detectors\n(polymorphic)",
        "SQLite\nStore",
        "Flask API",
        "Dashboard",
    ]

    colour = "#5aa9ff"
    n = len(stages)
    box_w, box_h = 0.1, 0.4
    gap = (1.0 - n * box_w) / (n + 1)

    for i, label in enumerate(stages):
        x = gap + i * (box_w + gap)
        y = 0.3
        rect = mpatches.FancyBboxPatch(
            (x, y),
            box_w,
            box_h,
            boxstyle="round,pad=0.01",
            facecolor=colour,
            edgecolor="white",
            linewidth=1.5,
        )
        ax.add_patch(rect)
        ax.text(
            x + box_w / 2,
            y + box_h / 2,
            label,
            ha="center",
            va="center",
            fontsize=8,
            color="white",
            fontweight="bold",
        )
        if i < n - 1:
            ax.annotate(
                "",
                xy=(x + box_w + gap, y + box_h / 2),
                xytext=(x + box_w, y + box_h / 2),
                arrowprops=dict(arrowstyle="->", color="white", lw=1.5),
            )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(
        "CloudShield X — System Architecture", color="#888888", fontsize=13, pad=10
    )

    out = OUT_DIR / "architecture.png"
    plt.savefig(out, dpi=200, transparent=True, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def make_evolution(versions: list[dict]):
    fig, ax = plt.subplots(figsize=(14, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.axis("off")

    n = len(versions)
    box_w, box_h = 0.11, 0.45
    gap = (1.0 - n * box_w) / (n + 1)

    for i, v in enumerate(versions):
        x = gap + i * (box_w + gap)
        y = 0.25
        colour = v["colour"]
        is_shipped = v["status"] == "shipped"

        if is_shipped:
            rect = mpatches.FancyBboxPatch(
                (x, y),
                box_w,
                box_h,
                boxstyle="round,pad=0.01",
                facecolor=colour,
                edgecolor=colour,
                linewidth=2,
                alpha=1.0,
            )
        else:
            rect = mpatches.FancyBboxPatch(
                (x, y),
                box_w,
                box_h,
                boxstyle="round,pad=0.01",
                facecolor="none",
                edgecolor=colour,
                linewidth=2,
                linestyle="dashed",
                alpha=0.45,
            )

        ax.add_patch(rect)
        ax.text(
            x + box_w / 2,
            y + box_h * 0.65,
            v["version"],
            ha="center",
            va="center",
            fontsize=9,
            color="white" if is_shipped else colour,
            fontweight="bold",
        )
        ax.text(
            x + box_w / 2,
            y + box_h * 0.3,
            v["steps"],
            ha="center",
            va="center",
            fontsize=7,
            color="white" if is_shipped else colour,
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("CloudShield X — Evolution Map", color="#888888", fontsize=13, pad=10)

    out = OUT_DIR / "evolution.png"
    plt.savefig(out, dpi=200, transparent=True, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


if __name__ == "__main__":
    versions = load_versions()
    make_architecture()
    make_evolution(versions)
    print("Both diagrams generated!")
