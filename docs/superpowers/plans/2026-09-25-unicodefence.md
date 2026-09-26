# UnicodeFence implementation plan

1. Add the package metadata and behavioral tests for clean text, zero-width
   characters, bidi controls, emoji false-positive protection, JSON output,
   invalid UTF-8, and CLI exit codes.
2. Run the test suite before adding production code and record the expected
   RED failure.
3. Implement the smallest pure scanner plus an argparse CLI with no runtime
   dependencies.
4. Run the suite again, then run ruff, mypy, build, package smoke, audit, and
   `git diff --check` as fresh commands.
5. Add the README, policy docs, example, verification record, and CI workflow.
6. Run a local end-to-end scan from an example file, initialize this separate
   repository, and run the security scan against the final worktree.
7. Commit, push the public repository, create `v0.1.0`, and confirm the remote
   commit, CI run, and release URL.
