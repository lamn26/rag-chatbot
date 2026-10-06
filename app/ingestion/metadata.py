from pathlib import Path

def enrich_metadata(
    metadata: dict,
    file_path: Path,
    chunk_index: int,
) -> dict:

    enriched = dict(metadata)

    enriched["source"] = str(file_path)
    enriched["filename"] = file_path.name
    enriched["chunk_index"] = chunk_index

    return enriched