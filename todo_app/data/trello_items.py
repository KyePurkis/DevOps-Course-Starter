import requests
import os
from todo_app.data.item import Item

API_KEY = os.getenv('API_KEY')
TOKEN = os.getenv('TOKEN')
BOARD_ID = os.getenv('BOARD_ID')
BASE_URL = 'https://api.trello.com/1'

def get_items():
    result = requests.get(f'{BASE_URL}/boards/{BOARD_ID}/lists', params={ 'cards': 'open', 'key': API_KEY, 'token': TOKEN})
    lists = result.json()
    data = []
    for l in lists:
        for card in l['cards']:
            data.append(Item.from_trello_card(card, l))
    return data