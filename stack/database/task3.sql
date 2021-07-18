SELECT customers.name
FROM "Orders" AS orders
         LEFT OUTER JOIN "OrderItems" AS orderItems
                         ON orderItems.row_id = orders.row_id
         LEFT OUTER JOIN "Customers" AS customers
                         ON customers.row_id = orders.customer_id
WHERE to_char(orders.registered_at, 'YYYY') = '2020'
  AND orderItems.name = 'Кассовый аппарат'