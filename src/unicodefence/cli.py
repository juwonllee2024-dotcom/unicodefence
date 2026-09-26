"""Command-line interface for UnicodeFence."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from .scanner import ScanResult, scan_file


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unicodefence",
        description="Reveal selected invisible Unicode controls before AI paste.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("scan", help="scan one explicitly chosen UTF-8 file")
    scan.add_argument("file", type=Path, help="file to inspect; it is never modified")
    scan.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def _format_text(result: ScanResult) -> str:
    title = "CLEAN" if result.status == "clean" else "REVIEW"
    lines = [
        f"UnicodeFence: {title}",
        f"file: {result.source}",
        f"findings: {len(result.findings)}",
    ]
    if not result.findings:
        lines.append("no selected invisible Unicode controls found")
    else:
        for finding in result.findings:
            lines.append(
                f"- line {finding.line}, column {finding.column}: "
                f"{finding.codepoint} {finding.name} [{finding.category}]"
            )
            lines.append(f"  context: {finding.context!r}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "scan":
        return 2

    try:
        result = scan_file(args.file)
    except UnicodeDecodeError as error:
        print(f"UnicodeFence: ERROR: input is not valid UTF-8 ({error})", file=sys.stderr)
        return 2
    except (OSError, ValueError) as error:
        print(f"UnicodeFence: ERROR: {error}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_format_text(result))
    return 1 if result.status == "review" else 0


if __name__ == "__main__":
    raise SystemExit(main())
