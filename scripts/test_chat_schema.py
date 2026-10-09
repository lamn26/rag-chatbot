from app.schemas.chat import ChatRequest, ChatResponse

def main():
    request = ChatRequest(
        question="What is the Transformer architecture?"
    )

    print("Request:")
    print(request.model_dump())

    response = ChatResponse(
        answer="The Transformer uses attention mechanisms.",
        sources=[
            {
                "filename": "Attention Is All You Need.pdf",
                "page_number": 2,
                "chunk_index": 24,
                "score": 0.8872,
            }
        ],
    )

    print("\nResponse:")
    print(response.model_dump())


if __name__ == "__main__":
    main()
