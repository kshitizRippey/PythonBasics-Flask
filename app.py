from datetime import datetime

import bcrypt
from flask import Flask, request

from db_ops import add_order, cancel_order, insert_user, update_order, get_order, get_products
from db_ops import get_user_id, get_stored_password
from handle_jwt import sign_jwt, is_logged_in

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return {'message': 'Hello World'}


@app.route("/signup", methods=['POST'])
def signup():
    username = request.json["username"]
    password = request.json["password"]
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    message = insert_user(username, hashed_password)
    return {"message": message}


@app.route("/login", methods=['POST'])
def login():
    response = {"message": "User does not exist!", "access_token": ""}
    username = request.json["username"]
    password = request.json["password"]
    password = password.encode('utf-8')
    hashed_password = get_stored_password(username)
    if hashed_password is not None:
        if bcrypt.checkpw(password, hashed_password):
            response["message"] = "Logged in successfully!"
            response["access_token"] = f"{sign_jwt(username)}"
        else:
            response["message"] = "Could not log in. Wrong Password!"
        return response
    return response


@app.route("/products", methods=['GET'])
def show_products():
    products = get_products()
    return products


@app.route("/create", methods=['POST'])
def create():
    token = request.json["token"]
    if is_logged_in(token):
        quantity = request.json["quantity"]
        user_id = get_user_id(token=token).get("user_id")
        result = add_order(quantity, datetime.now(), user_id, request.json["product_id"])
        return result
    else:
        return {"message": "User isn't logged in!"}


@app.route("/read", methods=['POST'])
def read():
    token = request.json["token"]
    if is_logged_in(token):
        order_id = request.json["order_id"]
        user_id = get_user_id(token).get("user_id")
        return get_order(order_id=order_id, user_id=user_id)
    else:
        return {"message": "User isn't logged in!"}


@app.route("/update", methods=['POST'])
def update():
    token = request.json["token"]
    if is_logged_in(token):
        order_id = request.json["order_id"]
        user_id = get_user_id(token).get("user_id")
        return update_order(order_id=order_id, quantity=request.json["quantity"], user_id=user_id)
    else:
        return {"message": "User isn't logged in!"}


@app.route("/delete", methods=['POST'])
def cancel():
    token = request.json["token"]
    if is_logged_in(token):
        order_id = request.json["order_id"]
        user_id = get_user_id(token).get("user_id")
        return cancel_order(order_id, user_id)
    else:
        return {"message": "User isn't logged in!"}


if __name__ == '__main__':
    app.run()
