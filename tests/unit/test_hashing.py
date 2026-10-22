import hashlib

from app.utils.hashing import calculate_sha256

def test_calculate_sha256_returns_correct_hash():
    content = b"test sentence"

    result = calculate_sha256(content)

    expected = hashlib.sha256(content).hexdigest()
    assert result == expected


def test_calculate_sha256_returns_64_character_hex_string():
    result = calculate_sha256(b"test content")

    assert len(result) == 64
    assert all(char in "0123456789abcdef" for char in result)


def test_calculate_sha256_handles_empty_bytes():
    result = calculate_sha256(b"")

    expected = hashlib.sha256(b"").hexdigest()
    assert result == expected


def test_calculate_sha256_changes_when_content_changes():
    hash_a = calculate_sha256(b"document A")
    hash_b = calculate_sha256(b"document a")

    assert hash_a != hash_b
