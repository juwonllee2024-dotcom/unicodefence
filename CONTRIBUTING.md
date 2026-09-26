# Contributing

Thank you for improving UnicodeFence.

1. Keep the scanner local-only and read-only.
2. Add a failing test before changing detection behavior.
3. Add both a positive fixture and a false-positive fixture when expanding the
   character set.
4. Run `python -m pytest -q`, `ruff check .`, `mypy`, `python -m build`, and
   `python -m pip_audit` before opening a pull request.
5. Never commit real private prompts, credentials, or copied customer data.

Small, focused pull requests are easiest to review.
