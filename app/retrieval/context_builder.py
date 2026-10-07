class ContextBuilder:
    def build(
        self,
        results,
    ) -> str:
        contexts = []

        for result in results:
            payload = result.payload or {}

            content = payload.get(
                "content",
                "",
            )

            file_name = payload.get(
                "filename",
                "unknown",
            )

            page_number = payload.get(
                "page_number",
                "unknown",
            )

            context = (
                f"[Source: {file_name}, page: {page_number}]\n"
                f"{content}"
            )

            contexts.append(context)

        return "\n\n---\n\n".join(
            contexts
        )