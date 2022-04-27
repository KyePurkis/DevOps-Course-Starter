import requests
import os
from todo_app.data.item import Item
from todo_app.data.status import ItemStatus

API_KEY = os.getenv('API_KEY')
TOKEN = os.getenv('TOKEN')
BOARD_ID = os.getenv('BOARD_ID')
BASE_URL = 'https://api.trello.com/1'

TODO_LIST_NAME = 'To Do'
DOING_LIST_NAME = 'Doing'
DONE_LIST_NAME = 'Done'

def get_items():
    lists = requests.get(f'{BASE_URL}/boards/{BOARD_ID}/lists', params={ 'cards': 'open', 'key': API_KEY, 'token': TOKEN}).json()
    data = []
    for l in lists:
        for card in l['cards']:
            data.append(Item.from_trello_card(card, list_name_to_status(l['name'])))
    data.sort(key=lambda x: x.status.value)
    return data

def add_item(name, desc):
    todo_list_id = get_list_id(TODO_LIST_NAME)
    requests.post(f'{BASE_URL}/cards', params={'idList': todo_list_id, 'name': name, 'desc': desc, 'key': API_KEY, 'token': TOKEN})


def doing_item(id):
    doing_list_id = get_list_id(DOING_LIST_NAME)
    requests.put(f'{BASE_URL}/cards/{id}', params={'idList': doing_list_id, 'key': API_KEY, 'token': TOKEN})

def complete_item(id):
    done_list_id = get_list_id(DONE_LIST_NAME)
    requests.put(f'{BASE_URL}/cards/{id}', params={'idList': done_list_id, 'key': API_KEY, 'token': TOKEN})

def get_list_id(name):
    lists = requests.get(f'{BASE_URL}/boards/{BOARD_ID}/lists', params={ 'key': API_KEY, 'token': TOKEN}).json()
    return next(x['id'] for x in lists if x['name'] == name)

def list_name_to_status(name):
    if name == TODO_LIST_NAME:
        return ItemStatus.TODO
    elif name == DOING_LIST_NAME:
        return ItemStatus.DOING
    elif name == DONE_LIST_NAME:
        return ItemStatus.DONE
    else:
        print('Found unknown status ', name)