"""Export all tables from riskregister.db to an Excel workbook.

Each SQLite table is written to its own worksheet in the output .xlsx file.
"""

from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path

import pandas as pd


INVALID_SHEET_CHARS = re.compile(r"[\\/*?:\[\]]")


def _safe_sheet_name(name: str) -> str:
    """Return an Excel-safe sheet name (max 31 chars, no invalid chars)."""
    cleaned = INVALID_SHEET_CHARS.sub("_", name).strip()
    if not cleaned:
        cleaned = "Sheet"
    return cleaned[:31]


def export_tables_to_excel(db_path: Path, output_path: Path) -> None:
    """Export every table in a SQLite database into separate Excel tabs."""
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    with sqlite3.connect(db_path) as conn:
        table_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        table_names = pd.read_sql_query(table_query, conn)["name"].tolist()

        if not table_names:
            raise ValueError(f"No tables found in database: {db_path}")

        used_sheet_names: dict[str, int] = {}

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for table_name in table_names:
                df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)

                base_sheet = _safe_sheet_name(table_name)
                suffix = used_sheet_names.get(base_sheet, 0)
                if suffix:
                    sheet_name = f"{base_sheet[:28]}_{suffix}"
                else:
                    sheet_name = base_sheet
                used_sheet_names[base_sheet] = suffix + 1

                df.to_excel(writer, sheet_name=sheet_name, index=False)


def _default_paths() -> tuple[Path, Path]:
    script_dir = Path(__file__).resolve().parent
    db_path = script_dir / "riskregister.db"
    output_path = script_dir / "riskregister_tables.xlsx"
    return db_path, output_path


def main() -> None:
    default_db, default_output = _default_paths()

    parser = argparse.ArgumentParser(
        description="Export all SQLite tables to one .xlsx file with separate tabs."
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=default_db,
        help=f"Path to SQLite DB file (default: {default_db})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=default_output,
        help=f"Output .xlsx path (default: {default_output})",
    )

    args = parser.parse_args()

    export_tables_to_excel(args.db, args.out)
    print(f"Created Excel export: {args.out}")


if __name__ == "__main__":
    main()
