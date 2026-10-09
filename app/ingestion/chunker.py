from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.embeddings.local import LocalEmbedding

class DocumentChunker:

    def __init__(self):
        self.splitter = SemanticChunker(
            embeddings=LocalEmbedding(),
            breakpoint_threshold_amount=0.9
        )

    def split(self, documents):

        return self.splitter.split_documents(
            documents
        )