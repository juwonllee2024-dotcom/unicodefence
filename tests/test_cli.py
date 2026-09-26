from pathlib import Path

from unicodefence.cli import main


def test_cli_clean_file_returns_zero(capsys, tmp_path: Path) -> None:
    path = tmp_path / "clean.txt"
    path.write_text("ordinary text\n", encoding="utf-8")

    assert main(["scan", str(path)]) == 0
    assert "UnicodeFence: CLEAN" in capsys.readouterr().out


def test_cli_review_file_returns_one_and_json(capsys, tmp_path: Path) -> None:
    path = tmp_path / "hidden.txt"
    path.write_text("ordinary\u200b text\n", encoding="utf-8")

    assert main(["scan", str(path), "--format", "json"]) == 1
    output = capsys.readouterr().out
    assert '"status": "review"' in output
    assert '"codepoint": "U+200B"' in output


def test_cli_invalid_utf8_returns_two(capsys, tmp_path: Path) -> None:
    path = tmp_path / "invalid.txt"
    path.write_bytes(b"valid\xff")

    assert main(["scan", str(path)]) == 2
    assert "UTF-8" in capsys.readouterr().err
