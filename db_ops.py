import logging
import sqlite3
from handle_jwt import decode_jwt


def get_connection(db_name) -> sqlite3.Connection:
    return sqlite3.connect(f"{db_name}.db")


def check_if_exists(conn, username):
    query = f'SELECT username FROM user WHERE username=?'
    cursor = conn.cursor()
    result = cursor.execute(query, (username,)).fetchone()
    return True if result is not None else False


def insert_user(username, password) -> str:
    try:
        with get_connection('python_basics') as conn:
            if check_if_exists(conn, username):
                return "User already exists!"
            cursor = conn.cursor()
            query = "INSERT INTO user(username, password) VALUES (?, ?)"
            cursor.execute(query, (username, password))
            status = False
            conn.commit()
            cursor.close()
            return "User created successfully!"
    except sqlite3.DatabaseError as e:
        logging.error(str(e))
    return "Internal Server Error"


def get_stored_password(username):
    with get_connection('python_basics') as conn:
        cursor = conn.cursor()
        query = f'SELECT password FROM user WHERE username=?'
        result = cursor.execute(query, (username,)).fetchone()
        if result is not None:
            return result[0]


def get_products():
    with get_connection('python_basics') as conn:
        cursor = conn.cursor()
        query = f'SELECT * FROM product'
        cursor.execute(query)
        result = [
            dict((cursor.description[i][0], value)
                 for i, value in enumerate(row))
            for row in cursor.fetchall()
        ]
        return result


def get_user_id(token):
    payload = decode_jwt(token)
    username = payload.get("username")
    with get_connection('python_basics') as conn:
        cursor = conn.cursor()
        query = f'SELECT user_id FROM user WHERE username=?'
        cursor.execute(query, (username,))
        result = dict((cursor.description[0][0], value) for value in cursor.fetchone())
        return result


def add_order(quantity, created_at, user_id, product_id):
    try:
        with get_connection('python_basics') as conn:
            cursor = conn.cursor()
            query = 'INSERT INTO "order"(quantity, created_at, user_id, product_id) VALUES(?,?,?,?)'
            cursor.execute(query, (quantity, str(created_at), user_id, product_id))
            conn.commit()
            return {"message": "Order created!", "order_id": cursor.lastrowid}
    except:
        return {"message": "Order couldn't be created!"}


def get_order(order_id: int, user_id: int):
    with get_connection('python_basics') as conn:
        cursor = conn.cursor()
        query = 'SELECT * FROM "order" WHERE order_id=? and user_id=?'
        cursor.execute(query, (order_id, user_id))
        result = cursor.fetchone()
        if result is None:
            return {"message": "Order doesn't exist!"}
        result = dict((cursor.description[i][0], value) for i, value in enumerate(result))
        return result


def update_order(quantity: int, order_id: int, user_id: int):
    with get_connection('python_basics') as conn:
        cursor = conn.cursor()
        query = 'UPDATE "order" SET quantity=? WHERE order_id=? AND user_id=?'
        cursor.execute(query, (quantity, order_id, user_id))
        conn.commit()
        if cursor.rowcount > 0:
            return {"message": "Order updated", "order_id": order_id}
        return {"message": "Order doesn't exist!"}


def cancel_order(order_id, user_id):
    with get_connection('python_basics') as conn:
        cursor = conn.cursor()
        query = 'DELETE FROM "order" WHERE order_id=? AND user_id=?'
        cursor.execute(query, (order_id, user_id))
        conn.commit()
        if cursor.rowcount == 0:
            return {"message": "Order doesn't exist!"}
        return {"message": "Order cancelled!", "order_id": order_id}
