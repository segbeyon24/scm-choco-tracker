Backend and Database Setup and Implementation
Here's a step-by-step guide to setting up the backend (Flask) and database (PostgreSQL) for your chocolate supply chain application:

1. Prerequisites
Python 3.8+: Ensure you have Python installed.  You can check with python3 --version.

pip: Python's package installer.  Usually comes with Python.  You can check with pip --version.

PostgreSQL: Install PostgreSQL on your system or have access to a PostgreSQL server.  Download from https://www.postgresql.org/download/.

AWS Account (Optional): If you plan to use AWS RDS, you'll need an AWS account.

2. Project Setup
Create a project directory:

mkdir chocolate_supply_chain
cd chocolate_supply_chain

Create a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate  # On Windows

Install Flask and psycopg2:

pip install Flask psycopg2

3. Database Setup (PostgreSQL)
Local PostgreSQL Setup:

Create a database:

Open a PostgreSQL terminal (e.g., psql).

Create a database:

CREATE DATABASE chocolate_db;

Create a user and grant privileges (replace your_user and your_password):

CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE chocolate_db TO your_user;

Configure database connection:

You'll need these credentials in your Flask application:

Host: localhost (or the actual host if it's not local)

Database: chocolate_db

User: your_user

Password: your_password

AWS RDS Setup (Optional):

Create an RDS instance:

Log in to the AWS Management Console.

Go to the RDS service.

Create a new PostgreSQL database instance.

Configure the instance settings (instance type, storage, security group).  Make sure the security group allows connections from your network.

Note down the endpoint (host), database name, username, and password.

Configure database connection:

Use the endpoint, database name, username, and password from the RDS instance in your Flask application.

4. Flask Application Setup
Create app.py:

```python
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection details (move to a separate config file or environment variables in production)
DB_HOST = 'localhost'  # Or your RDS endpoint
DB_NAME = 'chocolate_db'
DB_USER = 'your_user'
DB_PASSWORD = 'your_password'

def get_db_connection():
    """Get a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'OK'}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products from the database."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        # Convert the result to a list of dictionaries for JSON serialization
        products_list = []
        for product in products:
            products_list.append({
                'product_id': product[0],
                'name': product[1],
                'description': product[2],
                'manufacturer_id': product[3],
                'batch_number': product[4]
            })
        return jsonify({'products': products_list}), 200
    except Exception as e:
        print(f"Error fetching products: {e}")
        return jsonify({'error': f'Error fetching products: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product in the database."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Failed to connect to database'}), 500

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    manufacturer_id = data.get('manufacturer_id')
    batch_number = data.get('batch_number')

    if not all([name, description, manufacturer_id, batch_number]):
        return jsonify({'error': 'Missing required fields'}), 400

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO products (name, description, manufacturer_id, batch_number)
            VALUES (%s, %s, %s, %s)
            RETURNING product_id
            """,
            (name, description, manufacturer_id, batch_number)
        )
        product_id = cursor.fetchone()[0]  # Get the inserted product ID
        conn.commit()
        return jsonify({'message': 'Product created successfully', 'product_id': product_id}), 201
    except Exception as e:
        conn.rollback()
        print(f"Error creating product: {e}")
        return jsonify({'error': f'Error creating product: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
```

Explanation of app.py:

Imports Flask and psycopg2.

Defines database connection details.  Important: These should be moved to environment variables or a separate configuration file in a production environment for security.

get_db_connection():  A helper function to establish a database connection.

/api/health:  A simple endpoint to check if the application is running.

/api/products (GET):  Retrieves all products from the database and returns them as JSON.

/api/products (POST):  Creates a new product in the database.  It receives product data as JSON, inserts it into the products table, and returns the ID of the newly created product.


- Create Database Tables:

Create the necessary tables in your PostgreSQL database.  You can use a database management tool (e.g., pgAdmin) or execute SQL commands directly.  Here's an example:

```sql
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
```


```sql
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

\dt
```

5. Run the Application
Run the Flask application:

python app.py

The application will start running at `http://127.0.0.1:5000/`

6. Test the API

Health check:
```bash
curl [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health)
```

```bash
# Get products:
curl [http://127.0.0.1:5000/api/products](http://127.0.0.1:5000/api/products)

# Create a product (replace with actual data):
curl -X POST -H "Content-Type: application/json" \
-d '{"name": "Dark Chocolate", "description": "Premium dark chocolate", "manufacturer_id": 1, "batch_number": "BATCH001"}' \
[http://127.0.0.1:5000/api/products](http://127.0.0.1:5000/api/products)
```
