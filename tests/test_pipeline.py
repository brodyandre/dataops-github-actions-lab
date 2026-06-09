from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

import pytest

from dataops_pipeline.pipeline import (
    PipelineError,
    build_customer_segment,
    run_pipeline,
)

CSV_HEADER = "customer_id,customer_name,email,city,country,total_spent"


def write_customers_file(tmp_path: Path, rows: list[str]) -> Path:
    input_path = tmp_path / "customers.csv"
    input_path.write_text(
        "\n".join([CSV_HEADER, *rows]) + "\n",
        encoding="utf-8",
    )
    return input_path


def build_output_paths(tmp_path: Path) -> tuple[Path, Path]:
    return (
        tmp_path / "customers_processed.csv",
        tmp_path / "pipeline_summary.md",
    )


@pytest.mark.parametrize(
    ("total_spent", "expected_segment"),
    [
        (Decimal("1500.00"), "high_value"),
        (Decimal("300.00"), "medium_value"),
        (Decimal("299.99"), "low_value"),
    ],
)
def test_build_customer_segment_applies_thresholds(
    total_spent: Decimal, expected_segment: str
) -> None:
    assert build_customer_segment(total_spent) == expected_segment


def test_run_pipeline_rejects_missing_required_columns(tmp_path: Path) -> None:
    input_path = tmp_path / "customers.csv"
    output_path, report_path = build_output_paths(tmp_path)

    input_path.write_text(
        "\n".join(
            [
                "customer_id,customer_name,email,city,total_spent",
                "C001,Ana Silva,ana.silva@example.com,Sao Paulo,1500.00",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(PipelineError, match="Missing required columns: country"):
        run_pipeline(input_path, output_path, report_path)


def test_run_pipeline_writes_processed_customers_file(tmp_path: Path) -> None:
    input_path = write_customers_file(
        tmp_path,
        rows=[
            " C001 , Ana Silva , ana.silva@example.com , Sao Paulo , Brazil , 1500.00 ",
            "C002, Bruno Costa ,bruno.costa@example.com,Rio de Janeiro,Brazil,300.00",
            "C003, Carla Lima,carla.lima@example.com,Belo Horizonte,Brazil,299.99",
        ],
    )
    output_path, report_path = build_output_paths(tmp_path)

    result = run_pipeline(input_path, output_path, report_path)

    assert result.output_path == output_path
    assert result.processed_records == 3
    assert output_path.exists()

    with output_path.open("r", encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert rows == [
        {
            "customer_id": "C001",
            "customer_name": "Ana Silva",
            "email": "ana.silva@example.com",
            "city": "Sao Paulo",
            "country": "Brazil",
            "total_spent": "1500.00",
            "customer_segment": "high_value",
        },
        {
            "customer_id": "C002",
            "customer_name": "Bruno Costa",
            "email": "bruno.costa@example.com",
            "city": "Rio de Janeiro",
            "country": "Brazil",
            "total_spent": "300.00",
            "customer_segment": "medium_value",
        },
        {
            "customer_id": "C003",
            "customer_name": "Carla Lima",
            "email": "carla.lima@example.com",
            "city": "Belo Horizonte",
            "country": "Brazil",
            "total_spent": "299.99",
            "customer_segment": "low_value",
        },
    ]


def test_run_pipeline_creates_summary_report(tmp_path: Path) -> None:
    input_path = write_customers_file(
        tmp_path,
        rows=[
            "C001,Ana Silva,ana.silva@example.com,Sao Paulo,Brazil,1200.00",
            "C002,Bruno Costa,bruno.costa@example.com,Rio de Janeiro,Brazil,450.00",
            "C003,Carla Lima,carla.lima@example.com,Belo Horizonte,Brazil,200.00",
        ],
    )
    output_path, report_path = build_output_paths(tmp_path)

    result = run_pipeline(input_path, output_path, report_path)

    assert result.report_path == report_path
    assert report_path.exists()

    report_content = report_path.read_text(encoding="utf-8")
    assert "# Pipeline Summary" in report_content
    assert "- Processed records: 3" in report_content
    assert "| high_value | 1 |" in report_content
    assert "| medium_value | 1 |" in report_content
    assert "| low_value | 1 |" in report_content


def test_run_pipeline_rejects_invalid_total_spent(tmp_path: Path) -> None:
    input_path = write_customers_file(
        tmp_path,
        rows=[
            "C001,Ana Silva,ana.silva@example.com,Sao Paulo,Brazil,not_a_number",
        ],
    )
    output_path, report_path = build_output_paths(tmp_path)

    with pytest.raises(PipelineError, match="Invalid total_spent at line 2"):
        run_pipeline(input_path, output_path, report_path)
