CREATE TRIGGER IF NOT EXISTS deduct_from_product_on_order_trigger
    AFTER
        INSERT
    ON "order"
BEGIN
    UPDATE product
    SET quantity = quantity - NEW.quantity
    WHERE product_id = NEW.product_id;
END;

CREATE TRIGGER IF NOT EXISTS add_to_product_on_order_trigger
    AFTER
        DELETE
    ON "order"
BEGIN
    UPDATE product
    SET quantity = quantity + OLD.quantity
    WHERE product_id = OLD.product_id;
END;


CREATE TRIGGER IF NOT EXISTS canceled_orders_trigger
    AFTER
        DELETE
    ON "order"
BEGIN
    INSERT INTO canceled_orders (order_id, quantity, created_at, user_id, product_id)
    VALUES (OLD.order_id, OLD.quantity, OLD.created_at, OLD.user_id, OLD.product_id);
END;