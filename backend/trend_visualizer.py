"""Simple threat trend chart generation."""

from pathlib import Path

import matplotlib.pyplot as plt


class TrendVisualizer:
    """Creates PNG charts for dashboard/report consumption."""

    @staticmethod
    def create_bar_chart(values: dict, title: str, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        labels = list(values.keys())
        counts = list(values.values())

        plt.figure(figsize=(8, 4))
        plt.bar(labels, counts)
        plt.title(title)
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
