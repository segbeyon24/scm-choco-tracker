from flask import Flask, request, jsonify
import psycopg2
import os  # For environment variables

app = Flask(__name__)

# Database connection details from environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME', 'chocolate_db')  # Default if not set
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

if not all([DB_HOST, DB_USER, DB_PASSWORD]):
    raise ValueError("Missing database connection details in environment variables.")


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
        product_id = cursor.fetchone()[0]
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
    app.run(host='0.0.0.0', port=5000, debug=True)