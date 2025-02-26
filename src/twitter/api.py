"""
Integración con la API oficial de Twitter
"""
import tweepy
from typing import Optional
import logging
from src.config import Config

logger = logging.getLogger(__name__)

class TwitterAPI:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(
            Config.TWITTER_API_KEY,
            Config.TWITTER_API_SECRET
        )
        self.auth.set_access_token(
            Config.TWITTER_ACCESS_TOKEN,
            Config.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(self.auth)
        self.client = tweepy.Client(
            consumer_key=Config.TWITTER_API_KEY,
            consumer_secret=Config.TWITTER_API_SECRET,
            access_token=Config.TWITTER_ACCESS_TOKEN,
            access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET
        )

    async def post_tweet(self, text: str) -> Optional[str]:
        """
        Postear un tweet usando la API v2 con reintentos
        Returns: ID del tweet si fue exitoso, None si falló
        """
        max_retries = 3
        retry_delay = 5  # segundos
        
        for attempt in range(max_retries):
            try:
                # Si no es el primer intento, esperar antes de reintentar
                if attempt > 0:
                    logger.info(f"Reintentando postear tweet (intento {attempt + 1}/{max_retries})...")
                    await asyncio.sleep(retry_delay * attempt)
                
                response = self.client.create_tweet(text=text)
                tweet_id = response.data['id']
                logger.info(f"Tweet posteado exitosamente: {tweet_id}")
                return tweet_id
                
            except Exception as e:
                error_msg = str(e)
                
                # Manejar diferentes tipos de errores
                if "429" in error_msg:  # Rate limit
                    wait_time = 15 * (attempt + 1)  # Espera progresiva
                    logger.warning(f"Rate limit alcanzado, esperando {wait_time} segundos...")
                    await asyncio.sleep(wait_time)
                elif "403" in error_msg:  # Forbidden
                    if "duplicate" in error_msg.lower():
                        logger.error("Tweet duplicado detectado")
                        return None
                    logger.error("Error de permisos en la API")
                    return None
                else:
                    logger.error(f"Error posteando tweet: {error_msg}")
                    
                if attempt == max_retries - 1:
                    logger.error("Se agotaron los reintentos")
                    return None

    async def post_reply(self, text: str, reply_to_id: str) -> Optional[str]:
        """
        Responder a un tweet usando la API v2
        Returns: ID del tweet de respuesta si fue exitoso, None si falló
        """
        try:
            response = self.client.create_tweet(
                text=text,
                in_reply_to_tweet_id=reply_to_id
            )
            tweet_id = response.data['id']
            logger.info(f"Respuesta posteada exitosamente: {tweet_id}")
            return tweet_id
        except Exception as e:
            logger.error(f"Error posteando respuesta: {str(e)}")
            return None

    async def get_mentions(self, since_id: Optional[str] = None) -> list:
        """
        Obtener menciones recientes usando la API v2
        Returns: Lista de menciones
        """
        try:
            mentions = []
            response = self.client.get_users_mentions(
                id=self.client.get_me().data.id,
                since_id=since_id,
                tweet_fields=['created_at', 'conversation_id']
            )
            
            if response.data:
                for tweet in response.data:
                    mentions.append({
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'conversation_id': tweet.conversation_id
                    })
            
            logger.info(f"Obtenidas {len(mentions)} menciones nuevas")
            return mentions
        except Exception as e:
            logger.error(f"Error obteniendo menciones: {str(e)}")
            return []

    async def get_tweet_thread(self, conversation_id: str) -> list:
        """
        Obtener el hilo completo de un tweet para contexto
        Returns: Lista de tweets en el hilo
        """
        try:
            thread = []
            response = self.client.search_recent_tweets(
                query=f"conversation_id:{conversation_id}",
                tweet_fields=['created_at', 'conversation_id', 'in_reply_to_user_id']
            )
            
            if response.data:
                for tweet in response.data:
                    thread.append({
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at
                    })
            
            thread.sort(key=lambda x: x['created_at'])
            return thread
        except Exception as e:
            logger.error(f"Error obteniendo hilo: {str(e)}")
            return []