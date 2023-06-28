# import bcrypt
# from datetime import datetime
# from fastapi import FastAPI
# from models import User, CreateOrder, Order, UpdateOrder
# from db_ops import insert_user, get_stored_password, get_user_id
# from handle_jwt import sign_jwt, is_logged_in
# from db_ops import get_products, add_order, get_order, update_order, cancel_order
#
# app = FastAPI()
#
#
# @app.get("/")
# async def home():
#     return {"message": "Hello World"}
#
#
# @app.post("/signup")
# async def signup(user: User):
#     username = user.username
#     password = user.password
#     password = password.encode('utf-8')
#     hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
#     message = insert_user(username, hashed_password)
#     return {"message": message}
#
#
# @app.post("/login")
# async def login(user: User):
#     response = {"message": "User does not exist!", "access_token": ""}
#     password = user.password
#     password = password.encode('utf-8')
#     hashed_password = get_stored_password(user.username)
#     if hashed_password is not None:
#         if bcrypt.checkpw(password, hashed_password):
#             response["message"] = "Logged in successfully!"
#             response["access_token"] = f"{sign_jwt(user.username)}"
#         else:
#             response["message"] = "Could not log in. Wrong Password!"
#         return response
#     return response
#
#
# @app.get("/products")
# async def show_products():
#     products = get_products()
#     return products
#
#
# @app.post("/create")
# async def create(order: CreateOrder):
#     token = order.token
#     if is_logged_in(token):
#         quantity = order.quantity
#         user_id = get_user_id(token=token).get("user_id")
#         result = add_order(quantity, datetime.now(), user_id, order.product_id)
#         return result
#     else:
#         return {"message": "User isn't logged in!"}
#
#
# @app.post("/read")
# async def read(order: Order):
#     token = order.token
#     if is_logged_in(token):
#         order_id = order.order_id
#         user_id = get_user_id(token).get("user_id")
#         return get_order(order_id=order_id, user_id=user_id)
#     else:
#         return {"message": "User isn't logged in!"}
#
#
# @app.post("/update")
# async def update(order: UpdateOrder):
#     token = order.token
#     if is_logged_in(token):
#         order_id = order.order_id
#         user_id = get_user_id(token).get("user_id")
#         return update_order(order_id=order_id, quantity=order.quantity, user_id=user_id)
#     else:
#         return {"message": "User isn't logged in!"}
#
#
# @app.post("/delete")
# async def cancel(order: Order):
#     token = order.token
#     if is_logged_in(token):
#         order_id = order.order_id
#         user_id = get_user_id(token).get("user_id")
#         return cancel_order(order_id, user_id)
#     else:
#         return {"message": "User isn't logged in!"}
