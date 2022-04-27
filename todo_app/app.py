from flask import Flask, redirect, render_template, request

from todo_app.flask_config import Config
from todo_app.data.trello_items import get_items, add_item, complete_item as complete_trello_item, doing_item as doing_trello_item
from todo_app.data.status import ItemStatus

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template("index.html", items=items, ItemStatus=ItemStatus)

@app.route('/item', methods=["POST"])
def create_item():
    item_title = request.form.get('item_title')
    item_desc = request.form.get('item_desc')
    add_item(item_title, item_desc)
    return redirect('/')

@app.route('/item/<id>/complete')
def complete_item(id):
    complete_trello_item(id)
    return redirect('/')

@app.route('/item/<id>/doing')
def doing_item(id):
    doing_trello_item(id)
    return redirect('/')