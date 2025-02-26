import json
import os

def clean_tweets():
    # Leer el archivo actual
    with open('tweets_generados.json', 'r', encoding='utf-8') as f:
        tweets = json.load(f)

    # Filtrar y limpiar tweets
    cleaned_tweets = []
    for tweet in tweets:
        # Verificar longitud y contenido válido
        if len(tweet.get('content', '')) > 280 or not tweet.get('content', '').strip():
            continue

        # Verificar timestamp
        if not tweet.get('timestamp'):
            continue

        # Corregir URLs de Twitter si existe ID
        if tweet.get('twitter_id'):
            tweet['twitter_url'] = f"https://twitter.com/x/status/{tweet['twitter_id']}"

        cleaned_tweets.append(tweet)

    # Guardar tweets limpios
    with open('tweets_generados.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_tweets, f, ensure_ascii=False, indent=2)

    print(f"Se limpiaron los tweets. Total tweets válidos: {len(cleaned_tweets)}")

if __name__ == "__main__":
    clean_tweets()