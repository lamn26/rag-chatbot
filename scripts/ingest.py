from app.ingestion.pipeline import IngestionPipeline

folder_path = "data/raw"

def main():

    pipeline = IngestionPipeline()

    chunks = pipeline.process_folder(
        folder_path=folder_path
    )

    print(f"\nTotal chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks[:10]):

        print("\n" + "=" * 80)

        print(f"Chunk #{index + 1}")
        print(f"Chunk ID: {chunk.chunk_id}")
        print(f"Document ID: {chunk.document_id}")

        print("\nMetadata:")
        print(chunk.metadata)

        print("\nContent:")
        print(chunk.content)


if __name__ == "__main__":
    main()