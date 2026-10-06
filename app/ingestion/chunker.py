from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 200,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
            add_start_index=True,
        )

    def split(self, documents):

        return self.splitter.split_documents(
            documents
        )