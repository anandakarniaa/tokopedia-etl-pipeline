CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    price NUMERIC,
    seller TEXT,
    city TEXT,
    sold INTEGER,
    rating NUMERIC,
    revenue NUMERIC,
    price_category TEXT,
    popular_product BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);