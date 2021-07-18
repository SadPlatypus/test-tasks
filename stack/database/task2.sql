CREATE OR REPLACE FUNCTION calculate_total_price_for_orders_group(INTEGER)
    RETURNS INTEGER
AS
$$
BEGIN
    RETURN (
        WITH RECURSIVE tmp AS (
            SELECT *
            FROM "Orders" AS t1
            WHERE t1.row_id = $1

            UNION ALL

            SELECT t2.*
            FROM "Orders" AS t2
                     JOIN tmp ON tmp.row_id = t2.parent_id
        )

        SELECT SUM(orderItems.price)
        FROM "OrderItems" AS orderItems
                 RIGHT OUTER JOIN tmp ON orderItems.order_id = tmp.row_id
    );
END
$$ LANGUAGE plpgsql;
