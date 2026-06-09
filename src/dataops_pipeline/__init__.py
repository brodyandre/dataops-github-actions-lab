"""Core package for the DataOps example pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pipeline import PipelineResult


def run_pipeline(
    input_path: Path, output_path: Path, report_path: Path
) -> "PipelineResult":
    from .pipeline import run_pipeline as _run_pipeline

    return _run_pipeline(input_path, output_path, report_path)


__all__ = ["run_pipeline"]
