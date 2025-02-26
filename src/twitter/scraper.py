"""
Twitter Scraper usando Playwright para obtener menciones y respuestas
"""
import asyncio
from typing import List, Dict, Optional
import logging
from playwright.async_api import async_playwright
from datetime import datetime, timedelta
from src.config import Config

logger = logging.getLogger(__name__)

class TwitterScraper:
    def __init__(self):
        self.username = Config.TWITTER_USERNAME
        self.password = Config.TWITTER_PASSWORD
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self._is_logged_in = False

    async def _init_browser(self):
        """Inicializar el navegador y el contexto con configuración anti-detección"""
        try:
            if self.browser is None:
                logger.info("Iniciando nueva instancia de Playwright...")
                try:
                    playwright = await async_playwright().start()
                    if not playwright:
                        raise Exception("No se pudo iniciar Playwright")
                        
                    self.playwright = playwright
                    logger.info("Playwright iniciado correctamente")
                    
                    # Configurar argumentos del navegador para evitar detección
                    browser_args = [
                        '--disable-blink-features=AutomationControlled',
                        '--disable-features=IsolateOrigins,site-per-process',
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    ]
                    
                    logger.info("Iniciando navegador...")
                    # Iniciar el navegador
                    self.browser = await self.playwright.chromium.launch(
                        headless=True,
                        args=browser_args
                    )
                    
                    if not self.browser:
                        raise Exception("No se pudo iniciar el navegador")
                    logger.info("Navegador iniciado correctamente")
    
                    # Crear el contexto inmediatamente después del navegador
                    logger.info("Creando contexto del navegador...")
                    self.context = await self.browser.new_context(
                        viewport={'width': 1920, 'height': 1080},
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        color_scheme='dark',
                        locale='es-MX'
                    )
    
                    if not self.context:
                        raise Exception("No se pudo crear el contexto del navegador")
                    logger.info("Contexto del navegador creado correctamente")
    
                    # Modificar el navigator.webdriver
                    await self.context.add_init_script("""
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """)
    
                    # Crear la página
                    logger.info("Creando nueva página...")
                    self.page = await self.context.new_page()
                    if not self.page:
                        raise Exception("No se pudo crear la página")
                    logger.info("Página creada correctamente")
    
                    # Configurar timeouts
                    await self.page.set_default_timeout(60000)
                    await self.page.set_default_navigation_timeout(60000)
                    
                except Exception as e:
                    logger.error(f"Error crítico iniciando Playwright/Browser: {str(e)}")
                    # Limpiar recursos en caso de error
                    if self.playwright:
                        await self.playwright.stop()
                        self.playwright = None
                    return False
                
                # Configurar el contexto del navegador
                self.context = await self.browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    color_scheme='dark',
                    locale='es-MX'
                )
                
                # Modificar el navigator.webdriver
                await self.context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                """)
                
                self.page = await self.context.new_page()
                
                # Configurar timeouts más largos
                await self.page.set_default_timeout(60000)
                await self.page.set_default_navigation_timeout(60000)
                
                logger.info("Navegador inicializado correctamente")
                return True
            
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando el navegador: {str(e)}")
            # Limpiar recursos en caso de error
            self.browser = None
            self.context = None
            self.page = None
            return False

    async def _login(self) -> bool:
        """Iniciar sesión en Twitter con manejo mejorado de errores"""
        if self._is_logged_in:
            return True

        try:
            await self._init_browser()
            
            # Ir a la página de login
            logger.info("Navegando a la página de login...")
            await self.page.goto('https://twitter.com/i/flow/login', wait_until='domcontentloaded')
            await self.page.wait_for_load_state('networkidle')
            await self.page.wait_for_timeout(2000)  # Espera adicional

            # Ingresar usuario con reintento
            logger.info("Ingresando usuario...")
            for _ in range(3):  # 3 intentos
                try:
                    username_input = await self.page.wait_for_selector('input[autocomplete="username"]', timeout=5000)
                    await username_input.fill(self.username)
                    await self.page.get_by_role("button", name="Siguiente").click()
                    break
                except Exception as e:
                    logger.warning(f"Reintentando input de usuario: {str(e)}")
                    await self.page.wait_for_timeout(2000)

            # Ingresar contraseña con reintento
            logger.info("Ingresando contraseña...")
            for _ in range(3):  # 3 intentos
                try:
                    password_input = await self.page.wait_for_selector('input[type="password"]', timeout=5000)
                    await password_input.fill(self.password)
                    await self.page.get_by_role("button", name="Iniciar sesión").click()
                    break
                except Exception as e:
                    logger.warning(f"Reintentando input de contraseña: {str(e)}")
                    await self.page.wait_for_timeout(2000)

            # Esperar a que el login se complete
            logger.info("Esperando que el login se complete...")
            await self.page.wait_for_timeout(3000)
            
            # Verificar si el login fue exitoso buscando elementos de la página principal
            try:
                await self.page.wait_for_selector('[data-testid="SideNav_NewTweet_Button"]', timeout=5000)
                self._is_logged_in = True
                logger.info("Login exitoso en Twitter")
                return True
            except:
                logger.error("No se pudo verificar el login exitoso")
                return False

        except Exception as e:
            logger.error(f"Error en login de Twitter: {str(e)}")
            if self.page:
                try:
                    await self.page.screenshot(path="login_error.png")
                    logger.info("Screenshot de error guardado en login_error.png")
                except:
                    pass
            return False

    async def get_mentions(self, hours_ago: int = 1) -> List[Dict]:
        """
        Obtener menciones recientes mediante scraping
        Args:
            hours_ago: Cuántas horas atrás buscar
        Returns:
            Lista de menciones encontradas
        """
        if not await self._login():
            return []

        mentions = []
        try:
            logger.info("Navegando a la página de menciones...")
            search_query = f"@{self.username}"
            url = f"https://twitter.com/search?q={search_query}&f=live"
            
            # Usar timeouts más largos para la navegación
            await self.page.goto(url, timeout=60000)
            await self.page.wait_for_load_state('networkidle', timeout=60000)
            
            # Esperar a que aparezcan los tweets con timeout más largo
            logger.info("Esperando a que carguen los tweets...")
            try:
                await self.page.wait_for_selector('article[data-testid="tweet"]', timeout=30000)
            except Exception as e:
                logger.warning(f"No se encontraron tweets inicialmente: {str(e)}")
                return []

            # Scroll para cargar más tweets con manejo de errores
            logger.info("Cargando más tweets...")
            scroll_attempts = 3
            for attempt in range(scroll_attempts):
                try:
                    await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    await asyncio.sleep(3)  # Esperar más tiempo entre scrolls
                    
                    # Verificar si se cargaron nuevos tweets
                    new_tweets = await self.page.query_selector_all('article[data-testid="tweet"]')
                    logger.info(f"Encontrados {len(new_tweets)} tweets en el intento {attempt + 1}")
                    
                except Exception as e:
                    logger.warning(f"Error en scroll {attempt + 1}/{scroll_attempts}: {str(e)}")
                    continue

            # Extraer tweets con timeout extendido
            logger.info("Extrayendo tweets...")
            tweets = await self.page.query_selector_all('article[data-testid="tweet"]', timeout=30000)
            
            for tweet in tweets:
                try:
                    # Extraer timestamp
                    time_element = await tweet.query_selector('time')
                    timestamp = await time_element.get_attribute('datetime')
                    tweet_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    
                    # Verificar si el tweet está dentro del rango de tiempo
                    if tweet_time > datetime.now(tweet_time.tzinfo) - timedelta(hours=hours_ago):
                        # Extraer texto
                        text_element = await tweet.query_selector('[data-testid="tweetText"]')
                        text = await text_element.inner_text()
                        
                        # Extraer ID del tweet
                        link_element = await tweet.query_selector('a[href*="/status/"]')
                        href = await link_element.get_attribute('href')
                        tweet_id = href.split('/status/')[1]
                        
                        mentions.append({
                            'id': tweet_id,
                            'text': text,
                            'created_at': tweet_time.isoformat(),
                            'url': f"https://twitter.com/user/status/{tweet_id}"
                        })
                except Exception as e:
                    logger.error(f"Error procesando tweet individual: {str(e)}")
                    continue

            logger.info(f"Encontradas {len(mentions)} menciones mediante scraping")
            return mentions

        except Exception as e:
            logger.error(f"Error en scraping de menciones: {str(e)}")
            return []

    async def get_tweet_context(self, tweet_id: str) -> Optional[Dict]:
        """
        Obtener el contexto de un tweet (tweet original y respuestas)
        """
        if not await self._login():
            return None

        try:
            # Ir a la página del tweet
            url = f"https://twitter.com/user/status/{tweet_id}"
            await self.page.goto(url)
            await self.page.wait_for_load_state('networkidle')

            # Extraer tweet original
            original_tweet = await self.page.query_selector('article[data-testid="tweet"]')
            if original_tweet:
                text_element = await original_tweet.query_selector('[data-testid="tweetText"]')
                original_text = await text_element.inner_text()
                
                return {
                    'original_tweet': original_text,
                    'tweet_id': tweet_id,
                    'url': url
                }

        except Exception as e:
            logger.error(f"Error obteniendo contexto del tweet: {str(e)}")
            return None

    async def post_tweet(self, text: str) -> bool:
        """
        Postear un tweet mediante scraping
        Returns: True si el tweet se posteó exitosamente
        """
        if not await self._login():
            return False

        try:
            # Navegar a la página principal de Twitter
            await self.page.goto('https://twitter.com/home')
            await self.page.wait_for_load_state('networkidle')
            
            # Buscar y hacer clic en el botón de tweet
            tweet_button = await self.page.get_by_role("button", name="Tweet")
            await tweet_button.click()
            
            # Esperar a que aparezca el área de texto y escribir el tweet
            tweet_input = await self.page.get_by_role("textbox", name="Post")
            await tweet_input.fill(text)
            
            # Hacer clic en el botón de enviar
            post_button = await self.page.get_by_test_id("tweetButton")
            await post_button.click()
            
            # Esperar a que el tweet se publique
            await self.page.wait_for_timeout(2000)
            
            logger.info("Tweet posteado exitosamente mediante scraping")
            return True
            
        except Exception as e:
            logger.error(f"Error en scraping al postear tweet: {str(e)}")
            if self.page:
                try:
                    # Tomar screenshot para debug
                    await self.page.screenshot(path="error_screenshot.png")
                    logger.info("Screenshot guardado en error_screenshot.png")
                except:
                    pass
            return False

    async def close(self):
        """Cerrar el navegador y limpiar recursos de forma segura"""
        logger.info("Iniciando cierre del navegador...")
        try:
            # Cerrar la página primero si existe
            if self.page:
                try:
                    await self.page.bring_to_front()  # Asegurarse que la página esté activa
                    await self.page.evaluate('() => {}')  # Verificar que la página responde
                    await self.page.close()
                    logger.info("Página cerrada correctamente")
                except Exception as e:
                    logger.warning(f"Error cerrando página: {str(e)}")
                self.page = None

            # Cerrar el contexto si existe
            if self.context:
                try:
                    await self.context.close()
                    logger.info("Contexto cerrado correctamente")
                except Exception as e:
                    logger.warning(f"Error cerrando contexto: {str(e)}")
                self.context = None

            # Cerrar el navegador si existe
            if self.browser:
                try:
                    await self.browser.close()
                    logger.info("Navegador cerrado correctamente")
                except Exception as e:
                    logger.warning(f"Error cerrando navegador: {str(e)}")
                self.browser = None

            # Cerrar playwright si existe
            if hasattr(self, 'playwright') and self.playwright:
                try:
                    await self.playwright.stop()
                    logger.info("Playwright detenido correctamente")
                except Exception as e:
                    logger.warning(f"Error deteniendo playwright: {str(e)}")
                self.playwright = None

        except Exception as e:
            logger.error(f"Error durante el cierre del navegador: {str(e)}")
        finally:
            # Asegurarse de que todas las referencias sean limpiadas
            self.page = None
            self.context = None
            self.browser = None
            self.playwright = None
            self._is_logged_in = False
            logger.info("Limpieza de recursos completada")