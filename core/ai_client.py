"""
Cliente Ollama para Kuro AI.
Placeholder — se implementa en el siguiente milestone.
"""

from typing import Generator


class AIClient:
    def __init__(self, host: str = "http://localhost:11434", model: str = "qwen2.5:7b"):
        self.host = host
        self.model = model

    def chat(self, messages: list[dict]) -> Generator[str, None, None]:
        """Streaming de respuesta. Yield de tokens."""
        # TODO: implementar con ollama-python
        yield "Ollama no conectado aún. Próximo milestone."

    def is_available(self) -> bool:
        return False
