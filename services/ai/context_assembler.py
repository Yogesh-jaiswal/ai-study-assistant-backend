class ContextAssembler:

    def build_context(self, chunks: list[str]) -> str:
        return "\n\n---\n\n".join(
            content
            for content in chunks
        )