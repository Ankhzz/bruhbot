"""
Configuración principal del Bruh Bot
"""
from typing import Dict
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    # Twitter API Credentials
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET: str = os.getenv("TWITTER_API_SECRET", "")
    TWITTER_ACCESS_TOKEN: str = os.getenv("TWITTER_ACCESS_TOKEN", "")
    TWITTER_ACCESS_TOKEN_SECRET: str = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
    
    # Twitter Scraping Credentials
    TWITTER_USERNAME: str = os.getenv("TWITTER_USERNAME", "")
    TWITTER_PASSWORD: str = os.getenv("TWITTER_PASSWORD", "")
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_API_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    OPENROUTER_MODEL: str = "anthropic/claude-3-opus"  # Podemos cambiarlo a grok cuando esté disponible
    
    # Bot Configuration
    TWEET_INTERVAL_MIN: int = 30 * 60  # 30 minutos en segundos
    TWEET_INTERVAL_MAX: int = 60 * 60  # 60 minutos en segundos
    REPLY_INTERVAL: int = 5 * 60  # 5 minutos entre replies para evitar rate limits
    
    # Personalidad del Bot
    BOT_PERSONALITY: Dict[str, str] = {
        "name": "Bruh",
        "species": "Chihuahua negro (mini doberman style)",
        "traits": [
            "Sassy",
            "Corajudo",
            "Web3 Enthusiast",
            "Story Protocol Expert",
            "Spanglish Speaker"
        ],
        "catchphrases": [
            "¡Ay, no manches!",
            "*tiembla con actitud*",
            "BRUH... 🙄",
            "Wey, let me tell you about IP on the blockchain...",
            "Time to mark my territory on this thread! 💦",
            "*ladra en Web3*"
        ]
    }
    
    # Paths
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    TWEETS_HISTORY_FILE: str = os.path.join(DATA_DIR, "tweets_history.json")

    @classmethod
    def validate(cls) -> bool:
        """Validar que todas las configuraciones necesarias estén presentes"""
        required_vars = [
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET",
            "TWITTER_ACCESS_TOKEN",
            "TWITTER_ACCESS_TOKEN_SECRET",
            "TWITTER_USERNAME",
            "TWITTER_PASSWORD",
            "OPENROUTER_API_KEY"
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            raise ValueError(f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}")
        
        return True

    @classmethod
    def ensure_directories(cls) -> None:
        """Asegurar que existan todos los directorios necesarios"""
        os.makedirs(cls.DATA_DIR, exist_ok=True)