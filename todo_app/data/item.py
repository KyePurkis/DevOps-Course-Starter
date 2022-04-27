from todo_app.data.status import ItemStatus
from datetime import datetime
class Item:
    def __init__(self, id, name, status = ItemStatus.TODO, desc = ''):
        self.id = id
        self.name = name
        self.status = status
        self.desc = desc
    
    @classmethod
    def from_trello_card(cls, card, status):
        return cls(card['id'], card['name'], status, card['desc'])