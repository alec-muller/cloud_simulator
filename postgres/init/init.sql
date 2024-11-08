CREATE SCHEMA IF NOT EXISTS alec_warehouse;

CREATE TABLE IF NOT EXISTS alec_warehouse.tb_fact_sales (
    "order_id" bigint,
    "customer_id" bigint,
    "product_id" bigint,
    "quantity" integer,
    "price" float,
    "total_price" float,
    "order_date" date,
    "sys_hash" varchar(500),
    "sys_imported_at" timestamp,
    "sys_imported_from" varchar(500),
    "Year" varchar(4),
    "Month" varchar(2),
    "sys_updated_at" timestamp
);

CREATE TABLE IF NOT EXISTS alec_warehouse.tb_customer_summary (
    "customer_id" bigint,
    "total_orders" int,
    "avg_price" float,
    "total_quantity" int,
    "revenue" float,
    "avg_items_per_order" int,
    "avg_price_per_order" float,
    "avg_price_per_product" float
);

CREATE TABLE IF NOT EXISTS alec_warehouse.tb_product_summary (
    "product_id" bigint,
    "total_orders" int,
    "total_customers" int,
    "total_quantity" int,
    "avg_quantity" float,
    "avg_price" float,
    "avg_price_per_order" float,
    "total_revenue" float,
    "avg_revenue_per_order" float,
    "avg_revenue_per_unit" float
);
