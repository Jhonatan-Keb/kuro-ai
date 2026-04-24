"""
Búsqueda web para Kuro AI.
Placeholder — se implementa en el siguiente milestone.
"""


class WebSearch:
    def __init__(self, provider: str = "searxng", url: str = "http://localhost:8080"):
        self.provider = provider
        self.url = url

    def search(self, query: str, max_results: int = 3) -> list[dict]:
        """Devuelve lista de {title, url, snippet}."""
        # TODO: implementar
        return []

    def is_available(self) -> bool:
        return False
