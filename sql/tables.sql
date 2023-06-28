CREATE TABLE IF NOT EXISTS user
(
    user_id  integer PRIMARY KEY AUTOINCREMENT,
    username text unique,
    password text
);

CREATE TABLE IF NOT EXISTS product
(
    product_id integer PRIMARY KEY AUTOINCREMENT,
    name       text,
    sku        text UNIQUE,
    price      real,
    quantity   integer
);

INSERT INTO product (name, sku, price, quantity)
VALUES ('Product 1', 'SKU001', 10.99, 100);
INSERT INTO product (name, sku, price, quantity)
VALUES ('Product 2', 'SKU002', 19.99, 50);
INSERT INTO product (name, sku, price, quantity)
VALUES ('Product 3', 'SKU003', 5.99, 200);
INSERT INTO product (name, sku, price, quantity)
VALUES ('Product 4', 'SKU004', 14.99, 75);

CREATE TABLE IF NOT EXISTS "order"
(
    order_id   integer PRIMARY KEY AUTOINCREMENT,
    quantity   integer,
    created_at text,
    user_id    integer,
    product_id integer,
    foreign key (user_id) references user,
    foreign key (product_id) references product
);

CREATE TABLE IF NOT EXISTS canceled_orders
(
    order_id   integer PRIMARY KEY AUTOINCREMENT,
    quantity   integer,
    created_at text,
    user_id    integer,
    product_id integer,
    foreign key (user_id) references user,
    foreign key (product_id) references product
);

