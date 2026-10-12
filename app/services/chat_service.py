from pathlib import Path

from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.llm.base import BaseLLM

class ChatService:

    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        llm: BaseLLM,
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.llm = llm

        self.prompt_template = self._load_prompt()

    def _load_prompt(self) -> str:
        prompt_path = (
            Path(__file__).resolve().parent.parent / "prompts" / "rag.txt"
        )

        return prompt_path.read_text(encoding="utf-8")

    def chat(
        self,
        question: str,
        top_k: int,
        score_threshold: float | None = None,
    ) -> dict:
        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
            score_threshold=score_threshold
        )

        if not results:
            return {
                "answer": "I don't know based on the provided documents.",
                "sources": [],
            }

        context = self.context_builder.build(results=results)

        prompt = self.prompt_template.format(
            context=context,
            question=question
        )

        answer = self.llm.generate(prompt=prompt)

        sources = []

        for result in results:
            payload = result.payload or {}

            sources.append({
                "filename": payload.get("filename"),
                "page_number": payload.get("page_number"),
                "chunk_index": payload.get("chunk_index"),
                "score": result.score,
                "content": payload.get("content"),
            })

        return {
            "answer": answer,
            "sources": sources,
        }