import requests
from bs4 import BeautifulSoup
import json

sites = {
    "https://jorna.6bags.space/": {
        "name": "Джорна"
    },
    "https://granada.6bags.space/": {
        "name": "Гранада"
    },
    "https://selta.6bags.space/": {
        "name": "Сельта"
    },
    "https://betis.6bags.space/": {
        "name": "Бетіс"
    },
    "https://elche.6bags.space/": {
        "name": "Ельче"
    },
    "https://girona.6bags.space/": {
        "name": "Жирона"
    },
    "https://lorens.6bags.space/": {
        "name": "Лоренс"
    },
    "https://kangaroo.6bags.space/": {
        "name": "Кенгуру"
    },
    "https://alba.6bags.space/": {
        "name": "Альба"
    },
    "https://verona.6bags.space/": {
        "name": "Верона"
    },

    # "https://baellery.6bags.space/",
    # "https://baellery-mini.6bags.space/",
    # "https://simpl.6bags.space/",
    # "https://baellery-italli.6bags.space/",


    # "https://tik-tak.6bags.space/": {
    #     "name": "Куртка демесезонна"
    # },
    # "https://winter-jacket.6bags.space/": {
    #     "name": "Куртка зимова"
    # },


    # "https://pants.6bags.space/",
    # "https://belt.6bags.space/",
    # "https://cap.6bags.space/",
    # "https://open-gloves.6bags.space",
    # "https://close-gloves.6bags.space",
    # "https://knee-pads.6bags.space",
    # "https://baellery-italli.6bags.space/",
    # "https://wallet-mini.6bags.space/"
}

headers = {
        'authority': 'granada.6bags.space',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

def get_data():
    with open('prices.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for s in sites:
            r = requests.get(s, headers=headers)
            bs = BeautifulSoup(r.text, 'html.parser')

            old_price = bs.find('div', class_='old').find_all('span')[0].text
            new_price = bs.find('div', class_='new').find_all('span')[0].text

            description_title = bs.find('ul', class_ = 'char_list').find_all('b')
            description_text = bs.find('ul', class_ = 'char_list').find_all('p')

            description = ''

            for i in range(len(description_title)):
                description += f'{description_title[i].text.encode('latin1').decode('utf-8')} {description_text[i].text.encode('latin1').decode('utf-8')}\n'

            name = sites[s]['name']
            data[name]['oldprice'] = old_price
            data[name]['newprice'] = new_price
            data[name]['description'] = description

    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)