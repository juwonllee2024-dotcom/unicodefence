# UnicodeFence design

## Goal

Give a person a trustworthy answer to one question before they paste text into
an AI tool: “Does this file contain invisible Unicode controls that I cannot
see?”

## Non-goals for v0.1.0

- No browser extension, clipboard interception, model call, network request,
  upload, sanitization, or automatic deletion.
- No claim that clean text is safe from all prompt injection.
- No broad heuristic that flags normal emoji joiners or variation selectors.

## User flow

1. The user explicitly chooses a UTF-8 text file.
2. `unicodefence scan FILE` reads it locally and read-only.
3. The CLI reports `CLEAN`, `REVIEW`, or `ERROR`.
4. For a review, it prints each code point, Unicode name, line/column, and a
   context line where the invisible character is replaced with a visible
   marker.
5. A JSON mode makes the same evidence usable in scripts without changing
   the default human-readable output.

## Detection policy

The default set is intentionally narrow:

- zero-width space/non-joiner (`U+200B`, `U+200C`), word joiner (`U+2060`),
  and BOM (`U+FEFF`);
- bidirectional embeddings, overrides, and isolates (`U+202A`–`U+202E`,
  `U+2066`–`U+2069`);
- Unicode tag characters (`U+E0000`–`U+E007F`).

Zero-width joiner (`U+200D`) and variation selector (`U+FE0F`) are not findings
in the default mode because they occur in ordinary emoji and scripts. The
policy can be expanded in a later, explicitly named strict mode with fixtures
for false positives.

## Safety and privacy

- The input path is explicit; there is no directory walk.
- The scanner never executes, imports, uploads, or rewrites input.
- Errors are non-zero and visible; no empty “safe” result is synthesized.
- Text is not persisted. JSON context snippets are emitted only to the user’s
  chosen stdout and may contain sensitive text, so the README warns users to
  redirect output carefully.

## Acceptance criteria

- Clean UTF-8 input returns exit code 0.
- A supported invisible control returns exit code 1 and an exact finding.
- Invalid UTF-8 or a directory returns exit code 2 with an actionable error.
- Text and JSON output agree on the status and finding count.
- Tests, lint, typecheck, build, audit, and package smoke test pass.
