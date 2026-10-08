from app.llm.local import LocalLLM


def main():

    print("Loading local LLM...")

    llm = LocalLLM()

    prompt = """
        Explain what the Transformer architecture is in simple terms.
    """

    print("\nGenerating response...\n")

    response = llm.generate(prompt)

    print(response)


if __name__ == "__main__":
    main()