CREATE TABLE manufacturers (
    manufacturer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    manufacturer_id INTEGER REFERENCES manufacturers(manufacturer_id),
    batch_number VARCHAR(255) NOT NULL
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    contact_person VARCHAR(255)
);

CREATE TABLE cacao_batches (
    cacao_batch_id SERIAL PRIMARY KEY,
    supplier_id INTEGER REFERENCES suppliers(supplier_id),
    harvest_date DATE NOT NULL,
    quantity DECIMAL NOT NULL,
    certification VARCHAR(255)
);

CREATE TABLE product_cacao_batch (
    product_id INTEGER REFERENCES products(product_id),
    cacao_batch_id INTEGER REFERENCES cacao_batches(cacao_batch_id),
    PRIMARY KEY (product_id, cacao_batch_id)
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    event VARCHAR(255) NOT NULL,
    details JSONB
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  --  Store hashed passwords, not plain text
    role VARCHAR(255) NOT NULL
);