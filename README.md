# Kuro AI

Asistente de IA local con estética Dendro/Nahida. Se activa con la tecla Copilot (F24), funciona offline con Ollama y busca en la web cuando hay conexión.

## Stack

- **UI**: PyQt6 — ventana frameless glassmorphism, siempre encima
- **AI local**: Ollama (qwen2.5:7b o phi3.5:mini)
- **Búsqueda web**: SearXNG local o Tavily API
- **Hotkey**: KDE shortcut → F24 → lanza/oculta la ventana

## Estructura

```
kuro-ai/
├── main.py              # Punto de entrada
├── ui/
│   ├── window.py        # Ventana principal frameless
│   ├── chat_widget.py   # Área de mensajes con scroll
│   ├── bubble.py        # Burbujas de chat individuales
│   └── toolbar.py       # Barra inferior (chips, input, send)
├── core/
│   ├── ai_client.py     # Cliente Ollama (streaming)
│   ├── web_search.py    # Búsqueda web (SearXNG / Tavily)
│   └── settings.py      # Config persistente
├── config/
│   └── config.yaml      # Modelo, colores, hotkey, etc.
└── assets/
    └── icons/
```

## Instalación

```bash
pip install PyQt6 ollama httpx pyyaml
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b
python main.py
```

## Roadmap

- [x] Ventana frameless glassmorphism
- [x] UI de chat con burbujas animadas
- [x] Toolbar con chips web/offline
- [ ] Integración Ollama streaming
- [ ] Búsqueda web SearXNG
- [ ] Hotkey global F24
- [ ] Historial de conversaciones
