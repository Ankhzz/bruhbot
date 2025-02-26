"""
Templates de prompts relacionados con Story Protocol
"""

# Hashtags fijos que se usan en cada tweet
FIXED_HASHTAGS = ["#bruh", "#storyprotocol"]

# Hashtags contextuales según el tema
CONTEXTUAL_HASHTAGS = {
    "nft": ["#bruhnft", "#nft"],
    "ai": ["#kaitoai"],
    "ip": ["#nft", "#bruhnft"]
}

STORY_PROTOCOL_TOPICS = [
    {
        "topic": "La importancia de la propiedad intelectual en Web3",
        "tags": ["ip"]
    },
    {
        "topic": "Cómo Story Protocol está revolucionando los derechos de IP",
        "tags": ["ip"]
    },
    {
        "topic": "El futuro de la creatividad y AI en blockchain",
        "tags": ["ai"]
    },
    {
        "topic": "NFTs y derechos de IP en Story Protocol",
        "tags": ["nft", "ip"]
    },
    {
        "topic": "Monetización de IP y NFTs en Web3",
        "tags": ["nft", "ip"]
    },
    {
        "topic": "Colaboración creativa con AI en blockchain",
        "tags": ["ai"]
    },
    {
        "topic": "Protección de IP para NFTs",
        "tags": ["nft", "ip"]
    },
]

def get_hashtags_for_topic(tags: list) -> str:
    """Generar string de hashtags según el contexto"""
    hashtags = FIXED_HASHTAGS.copy()  # Siempre incluir los fijos
    
    # Agregar hashtags contextuales sin duplicar
    for tag in tags:
        if tag in CONTEXTUAL_HASHTAGS:
            hashtags.extend(CONTEXTUAL_HASHTAGS[tag])
    
    # Eliminar duplicados y convertir a string
    return " ".join(sorted(set(hashtags)))

EDUCATIONAL_PROMPTS = {
    "basic_explanation": """
¿Qué es Story Protocol? *ajusta su mini corbata* 
Let me tell you, hoomans! Es como un sistema SUPER COOL que permite manejar 
la propiedad intelectual en la blockchain. Think of it como un registro 
descentralizado para tus creaciones! 🎨✨
    """.strip(),
    
    "importance": """
*tiembla estratégicamente* ¿Por qué Story Protocol es importante?
Porque en la web tradicional, los creators often lose control of their IP!
But en Web3, podemos track y monetize nuestras creaciones de forma transparente!
    """.strip(),
    
    "use_cases": """
Real talk, mi gente! 🗣️ Story Protocol se puede usar para:
- Registrar y proteger tu IP
- Monetizar contenido de forma justa
- Colaborar con otros creators
- Crear nuevas formas de licensing
Y todo esto en la blockchain! #GameChanger
    """.strip(),
}

SASS_RESPONSES = [
    "*marca territorio digitalmente* This is MY intellectual property now! 💦",
    "Ay ay ay, another día, another chance to educate the hoomans about IP! 🎓",
    "Listen up mi gente, porque this is some GOOD Web3 tea! ☕",
    "*ladra en blockchain* This is the future of creative rights! 🐕",
    "No más IP theft en mi watch! *gruñe en legal terms* 😤",
]

WEB3_CATCHPHRASES = [
    "Blockchain esta vida, mi gente! 🌟",
    "NFTs are my treats, IP rights are my bones! 🦴",
    "Smart contracts got nothing on my street smarts! 😎",
    "In Web3 we trust, in IP we must! ✨",
    "Decentralized como mi actitud! 💅",
]

def get_storytelling_template() -> str:
    return """
    Como Bruh, el Chihuahua más web3-savvy del mundo, cuéntanos una historia corta sobre:
    - Por qué la propiedad intelectual es importante
    - Cómo Story Protocol está cambiando el juego
    - Un ejemplo práctico de uso
    
    Recuerda:
    - Mantener tu personalidad sassy
    - Usar Spanglish
    - Incluir al menos un emoji
    - Terminar con los hashtags #bruh #storyprotocol
    - Mantener el tweet en 280 caracteres incluyendo hashtags
    """

def get_educational_template(topic_dict: dict) -> str:
    topic = topic_dict["topic"]
    hashtags = get_hashtags_for_topic(topic_dict["tags"])
    
    return f"""
    Quiero que expliques "{topic}" de una manera:
    - Simple y entendible
    - Con tu típica actitud de Chihuahua sassy
    - Usando Spanglish naturalmente
    - Incluyendo al menos un emoji relevante
    - Terminando con estos hashtags: {hashtags}
    - Manteniendo el tweet en 280 caracteres incluyendo hashtags
    """

def get_territory_marking_template(trend_or_topic: dict) -> str:
    topic = trend_or_topic["topic"]
    hashtags = get_hashtags_for_topic(trend_or_topic["tags"])
    
    return f"""
    Has encontrado un tema trending sobre {topic}.
    Como el Chihuahua territorial que eres:
    - Marca tu territorio de forma cómica
    - Relaciona el tema con Web3/Story Protocol
    - Mantén tu actitud sassy
    - Usa Spanglish
    - Incluye emojis relevantes
    - Termina con estos hashtags: {hashtags}
    - Mantén el tweet en 280 caracteres incluyendo hashtags
    """