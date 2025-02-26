"""
Clase principal del Bruh Bot - El Chihuahua Web3 más sassy de Twitter
Versión API-only: Solo posting de tweets, sin scraping
"""
import json
import asyncio
import random
from datetime import datetime
from typing import Dict, List
import logging

from src.config import Config
from src.llm.openrouter import OpenRouterClient
from src.knowledge.prompts import story_protocol
from src.twitter.api import TwitterAPI

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BruhBot:
    def __init__(self):
        self.config = Config
        self.llm = OpenRouterClient()
        self.twitter_api = TwitterAPI()
        self.last_tweet_time = None
        self.tweets_history: List[Dict] = self._load_tweets_history()
        
        # Asegurarnos que existan los directorios necesarios
        self.config.ensure_directories()
        
        logger.info("Bot inicializado en modo API-only - *mueve la colita* ¡Listo para generar tweets!")

    def _load_tweets_history(self) -> List[Dict]:
        """Cargar historial de tweets del archivo JSON"""
        try:
            with open(self.config.TWEETS_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_tweets_history(self) -> None:
        """Guardar historial de tweets al archivo JSON"""
        with open(self.config.TWEETS_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tweets_history, f, ensure_ascii=False, indent=2)

    def _add_tweet_to_history(self, tweet: str, tweet_type: str) -> None:
        """Agregar un tweet al historial"""
        tweet_data = {
            "content": tweet,
            "type": tweet_type,
            "timestamp": datetime.now().isoformat()
        }
        self.tweets_history.append(tweet_data)
        self._save_tweets_history()

    def _get_random_interval(self) -> int:
        """Obtener un intervalo aleatorio entre tweets"""
        return random.randint(
            self.config.TWEET_INTERVAL_MIN,
            self.config.TWEET_INTERVAL_MAX
        )

    async def generate_tweet(self) -> str:
        """Generar un nuevo tweet con hashtags contextuales"""
        # 70% probabilidad de tweet sobre Story Protocol
        if random.random() < 0.7:
            # Seleccionar un topic aleatorio con sus tags
            topic_dict = random.choice(story_protocol.STORY_PROTOCOL_TOPICS)
            prompt = story_protocol.get_educational_template(topic_dict)
            tweet = await self.llm.generate_story_protocol_insight(prompt=prompt)
        else:
            # 30% probabilidad de tweet general/territorial
            # Para tweets generales, usar tags de NFT por defecto
            topic_dict = {"topic": "Bruh NFT Lifestyle", "tags": ["nft"]}
            prompt = story_protocol.get_territory_marking_template(topic_dict)
            tweet = await self.llm.generate_tweet(prompt=prompt)
        
        return tweet

    async def post_tweet(self, tweet: str) -> None:
        """Publicar un tweet usando la API de Twitter"""
        logger.info(f"Posteando tweet: {tweet}")
        
        try:
            # Usar la API para postear
            tweet_id = await self.twitter_api.post_tweet(text=tweet)
            if tweet_id:
                logger.info(f"Tweet posteado exitosamente con ID: {tweet_id}")
                self._add_tweet_to_history(tweet, "original")
            else:
                logger.error("No se pudo postear el tweet")
                
        except Exception as e:
            logger.error(f"Error posteando tweet: {str(e)}")

    async def run(self) -> None:
        """Ejecutar el bot en modo API-only"""
        logger.info("¡Bruh Bot iniciando en modo API-only! *tiembla con emoción*")
        
        try:
            while True:
                # Generar y postear tweet
                tweet = await self.generate_tweet()
                await self.post_tweet(tweet)
                
                # Esperar intervalo aleatorio
                interval = self._get_random_interval()
                minutes = interval / 60
                logger.info(f"Tweet posteado! Esperando {minutes:.1f} minutos hasta el próximo tweet... *se acurruca a dormir*")
                await asyncio.sleep(interval)
                
        except Exception as e:
            logger.error(f"Error en el bot: {str(e)}")
            raise

if __name__ == "__main__":
    # Validar configuración antes de iniciar
    Config.validate()
    
    # Iniciar el bot
    bot = BruhBot()
    asyncio.run(bot.run())