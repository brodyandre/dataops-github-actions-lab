from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, Mapping, Sequence

REQUIRED_COLUMNS = (
    "customer_id",
    "customer_name",
    "email",
    "city",
    "country",
    "total_spent",
)
SEGMENT_ORDER = ("high_value", "medium_value", "low_value")


class PipelineError(Exception):
    """Raised when the pipeline cannot safely process the input file."""


@dataclass(frozen=True)
class CustomerRecord:
    customer_id: str
    customer_name: str
    email: str
    city: str
    country: str
    total_spent: Decimal


@dataclass(frozen=True)
class ProcessedCustomerRecord:
    customer_id: str
    customer_name: str
    email: str
    city: str
    country: str
    total_spent: Decimal
    customer_segment: str


@dataclass(frozen=True)
class PipelineResult:
    processed_records: int
    output_path: Path
    report_path: Path


def clean_text(value: str | None) -> str:
    return (value or "").strip()


def ensure_required_columns(fieldnames: Sequence[str]) -> None:
    missing_columns = sorted(set(REQUIRED_COLUMNS).difference(fieldnames))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise PipelineError(f"Missing required columns: {missing}")


def parse_total_spent(raw_value: str, line_number: int) -> Decimal:
    try:
        return Decimal(raw_value)
    except InvalidOperation as exc:
        raise PipelineError(
            f"Invalid total_spent at line {line_number}: {raw_value}"
        ) from exc


def is_empty_row(row: Mapping[str | None, str | None]) -> bool:
    return all(clean_text(value) == "" for value in row.values())


def clean_row(row: Mapping[str | None, str | None]) -> dict[str, str]:
    return {
        clean_text(key): clean_text(value)
        for key, value in row.items()
        if key is not None
    }


def build_customer_record(
    cleaned_row: Mapping[str, str], line_number: int
) -> CustomerRecord:
    total_spent = parse_total_spent(cleaned_row.get("total_spent", ""), line_number)
    return CustomerRecord(
        customer_id=cleaned_row.get("customer_id", ""),
        customer_name=cleaned_row.get("customer_name", ""),
        email=cleaned_row.get("email", ""),
        city=cleaned_row.get("city", ""),
        country=cleaned_row.get("country", ""),
        total_spent=total_spent,
    )


def load_customers(input_path: Path) -> list[CustomerRecord]:
    if not input_path.exists():
        raise PipelineError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise PipelineError(
                f"Input file is empty or missing header: {input_path}"
            )

        reader.fieldnames = [clean_text(field) for field in reader.fieldnames]
        ensure_required_columns(reader.fieldnames)

        records: list[CustomerRecord] = []
        for line_number, row in enumerate(reader, start=2):
            if is_empty_row(row):
                continue

            cleaned_row = clean_row(row)
            records.append(build_customer_record(cleaned_row, line_number))

    return records


def build_customer_segment(total_spent: Decimal) -> str:
    if total_spent >= Decimal("1000"):
        return "high_value"
    if total_spent >= Decimal("300"):
        return "medium_value"
    return "low_value"


def transform_customers(
    records: Iterable[CustomerRecord],
) -> list[ProcessedCustomerRecord]:
    processed_records: list[ProcessedCustomerRecord] = []
    for record in records:
        processed_records.append(
            ProcessedCustomerRecord(
                customer_id=record.customer_id,
                customer_name=record.customer_name,
                email=record.email,
                city=record.city,
                country=record.country,
                total_spent=record.total_spent,
                customer_segment=build_customer_segment(record.total_spent),
            )
        )
    return processed_records


def write_processed_customers(
    records: Iterable[ProcessedCustomerRecord], output_path: Path
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "customer_id",
                "customer_name",
                "email",
                "city",
                "country",
                "total_spent",
                "customer_segment",
            ],
        )
        writer.writeheader()

        for record in records:
            writer.writerow(
                {
                    "customer_id": record.customer_id,
                    "customer_name": record.customer_name,
                    "email": record.email,
                    "city": record.city,
                    "country": record.country,
                    "total_spent": f"{record.total_spent:.2f}",
                    "customer_segment": record.customer_segment,
                }
            )

    return output_path


def build_summary_report(
    input_path: Path,
    output_path: Path,
    processed_records: Sequence[ProcessedCustomerRecord],
) -> str:
    segment_counts = Counter(record.customer_segment for record in processed_records)
    total_spent = sum(
        (record.total_spent for record in processed_records),
        start=Decimal("0"),
    )
    average_spent = (
        total_spent / Decimal(len(processed_records))
        if processed_records
        else Decimal("0")
    )

    lines = [
        "# Pipeline Summary",
        "",
        f"- Input file: `{input_path}`",
        f"- Output file: `{output_path}`",
        f"- Processed records: {len(processed_records)}",
        f"- Total spent: {total_spent:.2f}",
        f"- Average spent: {average_spent:.2f}",
        "",
        "## Customer segments",
        "",
        "| Segment | Customers |",
        "| --- | ---: |",
    ]

    for segment in SEGMENT_ORDER:
        lines.append(f"| {segment} | {segment_counts.get(segment, 0)} |")

    return "\n".join(lines) + "\n"


def write_summary_report(
    input_path: Path,
    output_path: Path,
    processed_records: Sequence[ProcessedCustomerRecord],
    report_path: Path,
) -> Path:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_content = build_summary_report(input_path, output_path, processed_records)
    report_path.write_text(report_content, encoding="utf-8")
    return report_path


def run_pipeline(
    input_path: Path,
    output_path: Path,
    report_path: Path,
) -> PipelineResult:
    customer_records = load_customers(input_path)
    processed_records = transform_customers(customer_records)
    written_output_path = write_processed_customers(processed_records, output_path)
    written_report_path = write_summary_report(
        input_path=input_path,
        output_path=written_output_path,
        processed_records=processed_records,
        report_path=report_path,
    )
    return PipelineResult(
        processed_records=len(processed_records),
        output_path=written_output_path,
        report_path=written_report_path,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a simple customer data pipeline."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/customers.csv"),
        help="Path to the raw CSV file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/customers_processed.csv"),
        help="Path to the processed CSV file.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/pipeline_summary.md"),
        help="Path to the Markdown summary report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = run_pipeline(args.input, args.output, args.report)
    except PipelineError as exc:
        print(f"Pipeline error: {exc}", file=sys.stderr)
        return 1

    print(f"Processed {result.processed_records} customers")
    print(f"Output file: {result.output_path}")
    print(f"Report file: {result.report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
