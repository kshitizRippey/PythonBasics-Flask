import random
import string

from app import app

client = app.test_client()
expired_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' \
                '.eyJ1c2VybmFtZSI6InRlc3R1c2VyMTIzIiwiZXhwaXJ5IjoxNjg3NzcyODEwLjEwNDE2Nn0' \
                '.YMBoMpg8jEGeZ5ipA2S98i7LyUpJzMuy_-Pbqpw5ujE'
valid_token = client.post("/login", json={"username": "test", "password": "test"}).get_json()["access_token"]


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello World"}


def test_signup_existing_user():
    response = client.post("/signup", json={"username": 'test', "password": 'test'})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User already exists!"}


def test_signup_new_user():
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    response = client.post("/signup", json={"username": random_string, "password": random_string})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User created successfully!"}


def test_login_correct_credentials():
    response = client.post("/login", json={"username": "testuser12", "password": "testuser12"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Logged in successfully!"
    assert "access_token" in response.get_json()
    assert "access_token" != ""


def test_wrong_password():
    response = client.post("/login", json={"username": "testuser12", "password": ""})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Could not log in. Wrong Password!", "access_token": ""}


def test_non_existing_user_login():
    response = client.post("/login", json={"username": "testuser1233", "password": "testuser1233"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User does not exist!", "access_token": ""}


def test_products_list():
    response = client.get("/products")
    assert response.status_code == 200
    assert type(response.get_json()) == list
    for i in response.get_json():
        assert type(i) == dict
        assert len(i) == 5


def test_create_order_with_expired_token():
    response = client.post("/create", json={"token": expired_token, "product_id": 2, "quantity": 10})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User isn't logged in!"}


def test_create_order_with_valid_token():
    response = client.post("/create", json={"token": valid_token, "product_id": 2, "quantity": 10})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Order created!"
    assert type(response.get_json()["order_id"]) is int


def test_check_order_with_valid_token():
    response = client.post("/read", json={"token": valid_token, "order_id": 19})
    assert response.status_code == 200
    assert type(response.get_json()["order_id"]) is int
    assert type(response.get_json()["order_id"]) is int
    assert type(response.get_json()["product_id"]) is int
    assert type(response.get_json()["user_id"]) is int
    assert type(response.get_json()["created_at"]) is str


def test_check_order_with_expired_token():
    response = client.post("/read", json={"token": expired_token, "order_id": 19})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User isn't logged in!"}


def test_check_non_existent_order():
    response = client.post("/read", json={"token": expired_token, "order_id": 100})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User isn't logged in!"}


# user x shouldn't be able to view order created by user y
def test_check_unauthorized_order_view():
    response = client.post("/read", json={"token": expired_token, "order_id": 19})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User isn't logged in!"}


def test_update_order_with_expired_token():
    response = client.post("/update", json={"token": expired_token, "order_id": 14, "quantity": 10})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User isn't logged in!"}


def test_update_order_with_unauthorized_user():
    response = client.post("/update", json={"token": valid_token, "order_id": 11, "quantity": 10})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Order doesn't exist!"}


# needs work
def test_update_order_with_authorized_user():
    order_id = 14
    response = client.post("/update", json={"token": valid_token, "order_id": order_id, "quantity": 15})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Order updated", "order_id": order_id}


def test_cancel_order_with_unauthorized_user():
    response = client.post("/delete", json={"token": expired_token, "order_id": 14})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User isn't logged in!"}


def test_cancel_order_with_non_existing_order():
    response = response = client.post("/delete", json={"token": valid_token, "order_id": 11})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Order doesn't exist!"}


def test_cancel_order_with_non_owner_user():
    response = client.post("/delete", json={"token": valid_token, "order_id": 38})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Order doesn't exist!"}


def test_cancel_order_with_authorized_user():
    order_id = 35
    response = client.post("/delete", json={"token": valid_token, "order_id": order_id})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Order cancelled!", "order_id": order_id}
