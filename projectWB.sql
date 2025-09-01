
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE sellers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

-- Shops table
CREATE TABLE shops (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);


CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);


CREATE TABLE skus (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category_id INTEGER REFERENCES categories(id),
    seller_id INTEGER REFERENCES sellers(id),
    shop_id INTEGER REFERENCES shops(id),
    brand_id INTEGER REFERENCES brands(id)
);


CREATE TABLE sku_stats (
    id SERIAL PRIMARY KEY,
    sku_id INTEGER REFERENCES skus(id),
    date VARCHAR(255),
    views INTEGER,
    orders INTEGER,
    sales FLOAT
);