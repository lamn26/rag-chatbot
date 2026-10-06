from pathlib import Path

from langchain_core.documents import Document as LangChainDocument
from unstructured.partition.auto import partition

class UnstructuredParser:

    def parse(
        self,
        file_path: Path,
    ) -> list[LangChainDocument]:

        elements = partition(
            filename=str(file_path),
        )

        documents = []

        for element in elements:

            text = str(element).strip()

            if not text:
                continue

            metadata = element.metadata.to_dict()

            metadata["source"] = str(file_path)
            metadata["filename"] = file_path.name

            documents.append(
                LangChainDocument(
                    page_content=text,
                    metadata=metadata,
                )
            )

        return documents