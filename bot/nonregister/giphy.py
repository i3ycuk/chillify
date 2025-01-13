from brain import GIPHY_API_KEY, requests, random, logging

def get_gif(query):
    logging.debug("Отправлен запрос GIF")
    url = f"https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": GIPHY_API_KEY,
        "q": query,
        "limit": 10,
        "rating": "pg"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        gifs = response.json().get("data", [])
        if gifs:
            return random.choice(gifs)["images"]["original"]["url"]
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе GIF: {e}")
        return None
