from unittest.mock import patch

from app.llm.cloud import CloudLLM
from app.llm.local import LocalLLM


def test_cloud_llm_generate():
    with patch("app.llm.cloud.genai.Client") as client_factory:
        client = client_factory.return_value
        client.models.generate_content.return_value.text = "Generated answer."

        llm = CloudLLM(model_name="test-model", temperature=0.25)
        response = llm.generate("Test prompt")

    assert response == "Generated answer."
    client.models.generate_content.assert_called_once()
    call = client.models.generate_content.call_args.kwargs
    assert call["model"] == "test-model"
    assert call["contents"] == "Test prompt"
    assert call["config"].temperature == 0.25


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