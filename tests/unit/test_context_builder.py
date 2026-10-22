from types import SimpleNamespace

from app.retrieval.context_builder import ContextBuilder

def make_result(payload):
    return SimpleNamespace(payload=payload)


def test_build_formats_single_result():
    results = [
        make_result({
            "content": "The Transformer uses attention.",
            "filename": "paper.pdf",
            "page_number": 3,
        })
    ]
    builder = ContextBuilder()

    context = builder.build(results)

    expected = (
        "[Source: paper.pdf, page: 3]\n"
        "The Transformer uses attention."
    )
    assert context == expected


def test_build_separates_multiple_results():
    results = [
        make_result({
            "content": "First chunk.",
            "filename": "paper.pdf",
            "page_number": 1,
        }),
        make_result({
            "content": "Second chunk.",
            "filename": "notes.txt",
            "page_number": 2,
        }),
    ]
    builder = ContextBuilder()

    context = builder.build(results)

    expected = (
        "[Source: paper.pdf, page: 1]\n"
        "First chunk.\n\n"
        "---\n\n"
        "[Source: notes.txt, page: 2]\n"
        "Second chunk."
    )
    assert context == expected


def test_build_returns_empty_string_for_no_results():
    builder = ContextBuilder()

    assert builder.build([]) == ""


def test_build_uses_defaults_when_metadata_is_missing():
    results = [
        make_result({"content": "Content without metadata."})
    ]
    builder = ContextBuilder()

    context = builder.build(results)

    # Assert
    expected = (
        "[Source: unknown, page: unknown]\n"
        "Content without metadata."
    )
    assert context == expected


def test_build_handles_none_payload():
    results = [make_result(None)]
    builder = ContextBuilder()

    context = builder.build(results)

    expected = (
        "[Source: unknown, page: unknown]\n"
    )
    assert context == expected
