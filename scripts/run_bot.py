#!/usr/bin/env python3
"""
Script principal para ejecutar el Bruh Bot
"""
import os
import sys
import signal
import asyncio
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Obtener la ruta al directorio src
src_dir = Path(__file__).resolve().parent.parent / 'src'

# Importar directamente desde la ruta relativa
sys.path.insert(0, str(src_dir.parent))

try:
    from src.bot import BruhBot
except ImportError as e:
    logger.error(f"Error importando BruhBot: {e}")
    logger.error(f"PYTHONPATH actual: {sys.path}")
    sys.exit(1)
from src.config import Config

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(Config.DATA_DIR, 'bruh_bot.log'))
    ]
)
logger = logging.getLogger(__name__)

# Variable global para el bot
bot = None

async def cleanup():
    """Limpieza de recursos al cerrar el bot"""
    logger.info("Iniciando proceso de cierre...")
    try:
        if bot:
            # Cerrar el scraper de Twitter
            if hasattr(bot, 'twitter_scraper'):
                logger.info("Cerrando Twitter Scraper...")
                await bot.twitter_scraper.close()
            
            # Guardar cualquier estado pendiente
            if hasattr(bot, 'tweets_history'):
                logger.info("Guardando historial de tweets...")
                bot._save_tweets_history()
    except Exception as e:
        logger.error(f"Error durante la limpieza: {str(e)}")
    finally:
        logger.info("Bruh Bot se despide! *tiembla por última vez* 👋")

async def main():
    """Función principal para ejecutar el bot"""
    try:
        # Validar configuración
        Config.validate()
        
        # Crear directorios necesarios
        Config.ensure_directories()
        
        # Inicializar y ejecutar el bot
        global bot
        bot = BruhBot()
        
        # Banner de inicio
        logger.info("""
░█▀▄░█▀▄░█░█░█░█░░░█▀▄░█▀█░▀█▀
░█▀▄░█▀▄░█░█░█▀█░░░█▀▄░█░█░░█░
░▀▀░░▀░▀░▀▀▀░▀░▀░░░▀▀░░▀▀▀░░▀░
        """)
        logger.info("¡El Chihuahua Web3 más sassy está despertando! 🐕✨")
        
        # Ejecutar el bot
        await bot.run()
        
    except Exception as e:
        logger.error(f"Error fatal en el bot: {str(e)}")
        await cleanup()
        sys.exit(1)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Interrupción detectada, cerrando...")
        loop.run_until_complete(cleanup())
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        loop.run_until_complete(cleanup())
    finally:
        loop.close()