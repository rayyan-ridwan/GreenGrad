"""Reporting helpers."""

from __future__ import annotations

from .tracker import ResourceSnapshot


def generate_markdown_report(snapshots: list[ResourceSnapshot]) -> str:
    """Generate a compact markdown report for a run."""
    if not snapshots:
        return "# GreenGrad Report\n\nNo snapshots recorded."

    avg_cpu = sum(snapshot.cpu_percent for snapshot in snapshots) / len(snapshots)
    avg_ram = sum(snapshot.ram_percent for snapshot in snapshots) / len(snapshots)

    gpu_values = [
        snapshot.gpu_power_watts
        for snapshot in snapshots
        if snapshot.gpu_power_watts is not None
    ]
    avg_gpu_power = sum(gpu_values) / len(gpu_values) if gpu_values else None

    lines = [
        "# GreenGrad Report",
        "",
        f"- Steps recorded: **{len(snapshots)}**",
        f"- Average CPU usage: **{avg_cpu:.2f}%**",
        f"- Average RAM usage: **{avg_ram:.2f}%**",
    ]

    if avg_gpu_power is None:
        lines.append("- Average GPU power: **N/A**")
    else:
        lines.append(f"- Average GPU power: **{avg_gpu_power:.2f} W**")

    return "\n".join(lines)
