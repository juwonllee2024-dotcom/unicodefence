# Security policy

## Scope

UnicodeFence is a local review aid, not a complete prompt-injection defense.
It intentionally detects a narrow set of invisible Unicode controls and does
not inspect every possible encoding, HTML/CSS hiding technique, or semantic
instruction.

## Reporting a vulnerability

Do not include copied private documents in a public issue. Please open a GitHub
security advisory or contact the repository owner through GitHub with:

- the affected version and platform;
- a minimal, non-sensitive reproduction;
- the expected and observed result;
- whether the issue can execute code, disclose input, or bypass a safety rule.

We will acknowledge reproducible reports and document a fix or limitation.
