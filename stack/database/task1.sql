CREATE OR REPLACE FUNCTION select_orders_by_item_name(TEXT)
    RETURNS table
            (
                order_id    INTEGER,
                customer    TEXT,
                items_count BIGINT
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT orderItems.order_id,
               customers.name         AS customer,
               COUNT(orderItems.name) AS items_count
        FROM "OrderItems" AS orderItems
                 LEFT OUTER JOIN "Orders" AS orders
                                 ON orders.row_id = orderItems.order_id
                 LEFT OUTER JOIN "Customers" AS customers
                                 ON customers.row_id = orders.customer_id
        WHERE orderItems.name = $1
        GROUP BY orderItems.order_id,
                 orderItems.name,
                 customers.name;
END
$$ LANGUAGE plpgsql;
