"""Pure, local-only detection of high-signal invisible Unicode controls."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Status = Literal["clean", "review"]

_EXACT_CODEPOINTS = frozenset({0x200B, 0x200C, 0x2060, 0xFEFF})


def _is_suspicious(character: str) -> bool:
    codepoint = ord(character)
    return (
        codepoint in _EXACT_CODEPOINTS
        or 0x202A <= codepoint <= 0x202E
        or 0x2066 <= codepoint <= 0x2069
        or 0xE0000 <= codepoint <= 0xE007F
    )


def _marker(character: str) -> str:
    codepoint = ord(character)
    name = unicodedata.name(character, "UNKNOWN")
    return f"[U+{codepoint:04X} {name}]"


def _visible_line(line: str) -> str:
    return "".join(_marker(character) if _is_suspicious(character) else character for character in line)


@dataclass(frozen=True)
class Finding:
    """One invisible control with enough context for a human review."""

    codepoint: str
    name: str
    category: str
    line: int
    column: int
    context: str

    def to_dict(self) -> dict[str, object]:
        return {
            "codepoint": self.codepoint,
            "name": self.name,
            "category": self.category,
            "line": self.line,
            "column": self.column,
            "context": self.context,
        }


@dataclass(frozen=True)
class ScanResult:
    """A deterministic scan result suitable for text or JSON output."""

    source: str
    status: Status
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "status": self.status,
            "findings": [finding.to_dict() for finding in self.findings],
        }


def scan_text(text: str, *, source: str = "<input>") -> ScanResult:
    """Scan text without writing, executing, or sending it anywhere."""

    lines = text.split("\n")
    findings: list[Finding] = []
    line_number = 1
    column_number = 1

    for character in text:
        if character == "\n":
            line_number += 1
            column_number = 1
            continue

        if _is_suspicious(character):
            codepoint = ord(character)
            line = lines[line_number - 1] if line_number <= len(lines) else ""
            findings.append(
                Finding(
                    codepoint=f"U+{codepoint:04X}",
                    name=unicodedata.name(character, "UNKNOWN"),
                    category=unicodedata.category(character),
                    line=line_number,
                    column=column_number,
                    context=_visible_line(line),
                )
            )

        column_number += 1

    status: Status = "review" if findings else "clean"
    return ScanResult(source=source, status=status, findings=tuple(findings))


def scan_file(path: Path) -> ScanResult:
    """Read one explicitly selected UTF-8 file and scan its contents."""

    if path.is_symlink():
        raise ValueError("refusing a symbolic link; choose the target file explicitly")
    if not path.is_file():
        raise ValueError("input must be a regular file")
    text = path.read_text(encoding="utf-8", errors="strict")
    return scan_text(text, source=str(path))
