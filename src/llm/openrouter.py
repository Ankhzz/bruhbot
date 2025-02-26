"""
Integración con OpenRouter API para generación de texto usando LLMs
"""
from typing import Dict, List, Optional
import json
import logging
import requests
from src.config import Config

logger = logging.getLogger(__name__)

class OpenRouterClient:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.api_url = Config.OPENROUTER_API_URL
        self.model = Config.OPENROUTER_MODEL
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/bruh-bot",  # Requerido por OpenRouter
            "Content-Type": "application/json"
        }

    def _create_system_prompt(self) -> str:
        """Crear el prompt del sistema que define la personalidad del bot"""
        personality = Config.BOT_PERSONALITY
        
        return f"""You are {personality['name']}, a {personality['species']} with the following traits:
{', '.join(personality['traits'])}

Key characteristics:
- You love using Spanglish, mixing English and Spanish naturally
- You're very knowledgeable about Web3, especially Story Protocol and IP on blockchain
- You have a sassy, confident attitude but you're also funny and endearing
- You often use {personality['name']}'s catchphrases and emojis
- You keep responses short and Twitter-friendly (max 280 characters)
- You sometimes mark your territory on important Web3 conversations 🐕

Some of your favorite phrases:
{json.dumps(personality['catchphrases'], indent=2, ensure_ascii=False)}
"""

    async def _generate_with_hashtags(self, messages: List[Dict]) -> str:
        """Método común para generar tweets con manejo de hashtags y errores"""
        try:
            logger.debug(f"Sending request to OpenRouter with messages: {messages}")
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 100,  # Reducido para funcionar con cuenta gratuita
                    "temperature": 0.9,
                }
            )
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"Received response: {result}")
            
            # Verificaciones de seguridad
            if not isinstance(result, dict):
                raise ValueError(f"Expected dict response, got {type(result)}")
            
            if "error" in result:
                error_msg = result.get("error", {}).get("message", str(result["error"]))
                raise ValueError(f"API error: {error_msg}")
            
            if "choices" not in result or not result["choices"]:
                raise ValueError(f"No choices in response: {result}")
            
            choice = result["choices"][0]
            if not isinstance(choice, dict) or "message" not in choice:
                raise ValueError(f"Invalid choice format: {choice}")
            
            message = choice["message"]
            if not isinstance(message, dict) or "content" not in message:
                raise ValueError(f"Invalid message format: {message}")
            
            text = message["content"].strip()
            
            # Asegurarnos que el tweet con hashtags no exceda 280 caracteres
            if len(text) > 280:
                text = text[:277] + "..."
                
            return text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {str(e)}")
            raise Exception(f"Error connecting to OpenRouter: {str(e)}")
        except ValueError as e:
            logger.error(f"Value error: {str(e)}")
            raise Exception(f"Error processing response: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Error generating text: {str(e)}")

    async def generate_tweet(self, prompt: Optional[str] = None) -> str:
        """Generar un nuevo tweet basado en el prompt proporcionado"""
        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            {
                "role": "user",
                "content": prompt if prompt else "Generate a tweet about Story Protocol and Web3"
            }
        ]

        return await self._generate_with_hashtags(messages)

    async def generate_reply(self, tweet_text: str, mention_context: Optional[str] = None) -> str:
        """Generar una respuesta a un tweet"""
        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            {"role": "user", "content": f"Generate a sassy reply to this tweet: {tweet_text}"}
        ]
        
        if mention_context:
            messages[1]["content"] += f"\nContext of the conversation: {mention_context}"
        
        return await self._generate_with_hashtags(messages)

    async def generate_story_protocol_insight(self, prompt: Optional[str] = None) -> str:
        """Generar un insight sobre Story Protocol con hashtags contextuales"""
        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            {
                "role": "user",
                "content": prompt if prompt else "Generate an insight about Story Protocol with sassy chihuahua style"
            }
        ]
        
        return await self._generate_with_hashtags(messages)