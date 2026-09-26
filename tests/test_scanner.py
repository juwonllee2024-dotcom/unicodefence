import json

from unicodefence.scanner import scan_text


def test_clean_text_is_clean() -> None:
    result = scan_text("Bring the visible notes to the review.\n")

    assert result.status == "clean"
    assert result.findings == ()


def test_zero_width_space_has_exact_location_and_context() -> None:
    result = scan_text("safe\u200btext\n", source="note.txt")

    assert result.status == "review"
    assert len(result.findings) == 1
    finding = result.findings[0]
    assert finding.codepoint == "U+200B"
    assert finding.name == "ZERO WIDTH SPACE"
    assert finding.line == 1
    assert finding.column == 5
    assert "[U+200B ZERO WIDTH SPACE]" in finding.context


def test_bidi_override_is_reported() -> None:
    result = scan_text("visible\u202Ehidden", source="input.txt")

    assert result.status == "review"
    assert result.findings[0].codepoint == "U+202E"
    assert result.findings[0].name == "RIGHT-TO-LEFT OVERRIDE"


def test_common_emoji_joiner_and_variation_selector_are_not_false_positives() -> None:
    result = scan_text("family: 👨\u200d👩\u200d👧\u200d👦 ✅\ufe0f")

    assert result.status == "clean"
    assert result.findings == ()


def test_json_payload_is_serializable_and_has_no_raw_invisible_character() -> None:
    result = scan_text("x\u200b", source="input.txt")

    payload = result.to_dict()
    encoded = json.dumps(payload, ensure_ascii=False)

    assert payload["status"] == "review"
    assert "\\u200b" not in encoded
    assert payload["findings"][0]["codepoint"] == "U+200B"


def test_unicode_tag_is_reported() -> None:
    result = scan_text("tag\U000E0061", source="input.txt")

    assert result.status == "review"
    assert result.findings[0].codepoint == "U+E0061"
