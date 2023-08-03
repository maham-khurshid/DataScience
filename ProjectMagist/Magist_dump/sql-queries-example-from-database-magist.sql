Select *
from orders;
---------total number of order dataset-----
SELECT 
    COUNT(*) AS orders_count
FROM
    orders;
    
    SELECT 
    COUNT(order_id) 
FROM
    orders;
    
    
    --------order status-------
    
    SELECT 
    order_status, 
    COUNT(*) AS orders
FROM
    orders
GROUP BY order_status;


-----user growth of magist----

SELECT 
    YEAR(order_purchase_timestamp) AS year_,
    MONTH(order_purchase_timestamp) AS month_,
    COUNT(customer_id)
FROM
    orders
GROUP BY year_ , month_
ORDER BY year_ , month_;

-----number of products-----

SELECT 
    COUNT(DISTINCT product_id) AS products_count
FROM
    products;
    
    select *
    from products;
    
    select count(product_name_length)
    from products;
    
    
    ------category with most products ---
    
    SELECT 
    product_category_name, 
    COUNT(DISTINCT product_id) AS n_products
FROM
    products
GROUP BY product_category_name
ORDER BY COUNT(product_id) DESC;

select *
from product_category_name_translation;

----How many of those products were present in actual transactions----

SELECT 
	count(DISTINCT product_id) AS n_products
FROM
	order_items;
    
    select *
    from order_items;
    
    -----most expensive and cheapest products price----
    
    SELECT 
    MIN(price) AS cheapest, 
    MAX(price) AS most_expensive
FROM 
	order_items;
    
       select order_id
    from order_items
    where price = 6735;
    
    Select *
from order_items;

     select product_id
    from order_items
    where price = 6735;
    
Select product_category_name
from products
where product_id = '489ae2aa008f021502940f251d4cce7f';

  select product_id
    from order_items
    where price = 0.85;
    
select *
from product_category_name_translation;

------ highest and lowest payment values------

SELECT 
	MAX(payment_value) as highest,
    MIN(payment_value) as lowest
FROM
	order_payments;
    
   ---------- Maximum someone has paid for an order--------
SELECT
    SUM(payment_value) AS highest_order
FROM
    order_payments
GROUP BY
    order_id
ORDER BY
    highest_order DESC
LIMIT
    1;
    
    
    select order_id
    from order_payments
    where payment_value = 13664.099609375;
    
    select product_id
    from order_items
    where order_id = '03caa2c082116e1d31e67e9ae3700499';
    
    select product_category_name
    from products
    where product_id = '5769ef0a239114ac3a854af00df129e4';
    
    