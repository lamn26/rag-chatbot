from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.llm.local import LocalLLM

def main():
    embedding_model = LocalEmbedding()

    vector_store = QdrantVectorStore(
        collection_name="documents"
    )

    retriever = Retriever(
        embedding_model=embedding_model,
        vector_store=vector_store
    )

    context_builder = ContextBuilder()

    llm = LocalLLM()

    question = "What is the Transformer architecture?"

    results = retriever.retrieve(
        query=question,
        top_k=5,
        score_threshold=0.825
    )

    context = context_builder.build(results=results)

    prompt = f"""
        You are a question-answering system that must strictly follow the provided context.

        IMPORTANT RULES:
        - The context is the ONLY source of truth.
        - You must NOT use your own knowledge, memory, or assumptions.
        - If the context is empty, you MUST NOT answer the question.
        - If the answer is not explicitly supported by the context, respond exactly:
        "I don't know based on the provided documents."
        - Never guess or infer an answer from outside knowledge.

        Context:
        {context}

        Question:
        {question}

        Answer:
    """

    answer = llm.generate(prompt=prompt)

    print("\n" + "-" * 80)
    print("QUESTION")
    print("-" * 80)
    print(question)

    print("\n" + "-" * 80)
    print("ANSWER")
    print("-" * 80)
    print(answer)


if __name__ == "__main__":
    main()