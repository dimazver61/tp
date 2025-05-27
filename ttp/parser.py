import requests


def search(query: str = 'Карта сокровищ Мертв') -> dict:
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,lb;q=0.6',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://eso-hub.com',
        'priority': 'u=1, i',
        'referer': 'https://eso-hub.com/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'page': '1',
        'lang': 'ru',
    }

    json_data = {
        'query': query,
        'sort': 'last_seen_at',
        'sort_dir': 'desc',
        'server': 'EU',
        'last_seen_at': None,
    }

    response = requests.post('https://trading.eso-hub.com/api/search/trade/listings',
                             params=params, headers=headers, json=json_data)

    response.raise_for_status()
    return response.json()

