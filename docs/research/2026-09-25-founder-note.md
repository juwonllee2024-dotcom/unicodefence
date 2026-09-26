# Founder note — 2026-09-25

## Today’s problem

People copy text from a web page, document, issue, or tool output into an AI
chat or coding agent. A person sees ordinary text, while the model may receive
non-printing Unicode controls that are impossible to review by eye. The first
use case is deliberately narrow: inspect a selected text file before it is
sent to an AI system.

## Evidence and limits

- OWASP describes prompt injection as a case where untrusted input changes an
  LLM’s intended behavior and specifically lists Unicode smuggling with
  invisible characters as an attack pattern:
  <https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html>
- A public Llama issue documents prompt-filter bypass experiments involving
  zero-width and directional-override characters:
  <https://github.com/meta-llama/llama/issues/1382>
- NVIDIA SkillSpector tracks hidden instructions padded with whitespace and
  discusses zero-width characters, comments, and encoded blobs as review
  blind spots:
  <https://github.com/NVIDIA/skillspector/issues/20>
- A public Librefang issue shows the opposite failure mode: treating every
  invisible-looking Unicode character as malicious can flag normal emoji
  sequences. UnicodeFence therefore uses a narrow default rule set and labels
  findings for review; it does not claim to prove that text is safe:
  <https://github.com/librefang/librefang/issues/7750>

These sources establish a real security and review problem, not demand for
this particular product. Adoption, false-positive rate, and protection in a
browser extension remain unverified.

## Four independent candidates

Scores are 1–5 for pain, novelty, buildability today, organic shareability,
and open-source fit.

| Candidate | Current fact | Innovation hypothesis | Different one thing | 7-day experiment | Score |
| --- | --- | --- | --- | ---: | ---: |
| **UnicodeFence** | Invisible Unicode can be present in AI input, but humans cannot reliably review it. | A 10-second local scan before paste can stop the most surprising class of hidden-input mistakes. | Shows the exact code point, location, and visible context without uploading text. | Ask 5 AI-heavy developers to scan one real copied file and record findings plus false positives. | **5/4/5/4/5 = 23** |
| LicenseLens | Developers often copy snippets without knowing attribution obligations. | A local pre-commit notice could prevent avoidable license mistakes. | Reports evidence instead of guessing a license. | Compare 20 copied snippets with their source licenses. | 3/2/4/3/4 = 16 |
| ContextBudget | AI users lose time when selected files exceed a model’s context budget. | A deterministic local size-and-token estimate could prevent failed requests. | Works before any provider is chosen. | Compare predicted and actual request sizes across 3 providers. | 4/3/5/3/4 = 19 |
| ChangeReceipt | Developers forget why a small AI-assisted change was made. | A one-command receipt could make review conversations easier. | Stores intent beside a diff without executing or submitting it. | Attach receipts to 10 small changes and ask reviewers if they use them. | 4/2/4/3/4 = 17 |

## Selection

UnicodeFence wins because it has a sharp, visible before/after moment, can be
useful with no model or cloud account, and is small enough to test honestly in
one run. LicenseLens and ChangeReceipt are useful but crowded by existing
portfolio tools; ContextBudget overlaps `promptparcel` and `tab2patch`.

The name `pasteguard` was rejected after checking GitHub because an unrelated
project already uses it and has substantial adoption. `unicodefence` had no
repository result for the owner at selection time.

## Business hypothesis

- First users: developers, security-minded researchers, and AI power users who
  paste external text into chat or coding agents.
- First ten users: local developer communities, AI-security issue threads, and
  people already using the owner’s context/AI tooling projects.
- Retention hypothesis: the command becomes a pre-paste habit when it catches
  one surprising hidden character in a real file.
- Revenue hypothesis: the core scanner stays free and open; teams may later
  pay for policy packs, CI reporting, or managed browser integrations. No
  revenue is assumed from this MVP.
