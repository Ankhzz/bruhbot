# Bruh Bot 🐕

El Chihuahua Web3 más sassy de Twitter. Un bot que genera tweets y respuestas con actitud sobre Story Protocol, NFTs y Web3.

## Características ✨

- Personalidad única de Chihuahua Web3-savvy
- Tweets automáticos sobre Story Protocol y derechos de IP
- Uso de Spanglish natural
- Integración con OpenRouter LLM para generación de texto
- Manejo de hashtags contextuales

## Tecnologías 🛠️

- Python 3.10+
- OpenRouter API para generación de texto
- Twitter API v2 para posting
- Playwright para web scraping (opcional)

## Configuración 🚀

1. Clona el repositorio:
```bash
git clone https://github.com/yourusername/bruh-bot.git
cd bruh-bot
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
- Copia `.env.example` a `.env`
- Llena las variables necesarias:
  - OPENROUTER_API_KEY
  - TWITTER_API_KEY
  - TWITTER_API_SECRET
  - TWITTER_ACCESS_TOKEN
  - TWITTER_ACCESS_SECRET

4. Ejecuta el bot:
```bash
python scripts/run_bot.py
```

## Estructura del Proyecto 📁

```
bruh-bot/
├── data/               # Datos y logs del bot
├── scripts/           # Scripts de ejecución
├── src/               # Código fuente
│   ├── knowledge/     # Prompts y conocimiento del bot
│   ├── llm/          # Integración con OpenRouter
│   └── twitter/       # Integración con Twitter
└── tests/            # Tests unitarios
```

## Contribuir 🤝

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia 📝

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.