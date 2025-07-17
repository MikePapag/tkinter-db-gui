import os
from dotenv import load_dotenv
import mysql.connector
from flask import Flask, request, jsonify
from functools import wraps

load_dotenv()
app = Flask(__name__)



user = os.getenv('MYSQL_USER')
host = os.getenv('MYSQL_HOST')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DB')
admin_key = os.getenv('ADMIN_API_KEY')
user_key = os.getenv('USER_API_KEY')

def require_api_key(allowed_methods):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('x-api-key')

            if not api_key:
                return jsonify({"error":"API key is missing"}), 401
            if api_key == admin_key:
                return f(*args, **kwargs)
            elif api_key == user_key:
                if request.method not in allowed_methods:
                    return jsonify({'error':f'Access dinied for {request.method} method'}),403
                return f(*args, **kwargs)
            else:
                return jsonify({'error':'Invalid API key'}),403
        return decorated_function
    return decorator

def get_db_connection():
    return mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database
)

@app.route('/verify-key', methods=['GET'])
def verify_key():
    api_key = request.headers.get('x-api-key')
    if api_key == admin_key:
        return jsonify({'role':'admin'}),200
    elif api_key == user_key:
        return jsonify({'role':'user'}),200
    else:
        return jsonify({'error':'Invalid API key'}),401

@app.route('/<table>/<int:id>', methods=['DELETE'])
@require_api_key(['GET','POST'])
def delete_row(table, id):
    allowed_tables = {'boats', 'boats_2', 'boats_3'}
    if table not in allowed_tables:
        return jsonify({'error': 'Invalid table name'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id = %s", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': 'No record found with that ID'}), 404

    return jsonify({'message': f'Row with id {id} deleted from {table}'}), 200

@app.route('/<table>', methods=['POST'])
@require_api_key(['GET','POST'])
def add_row(table):
    allowed_tables = {"boats", "boats_2", "boats_3"}
    if table not in allowed_tables:
        return jsonify({'error': 'Invalid table name'}),400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    moving = data.get('moving')
    id = data.get('id')

    if None in [name, latitude, longitude, moving]:
        return jsonify({'Error':'Missing required fields'}), 400
    try:
        query = f"INSERT INTO {table} (id, name, latitude, longitude, moving) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query,(id, name, latitude, longitude, moving))
        conn.commit()
        return jsonify({'message':f'New row added to {table}'}),201
    except Exception as e:
        return jsonify({'error': str(e)}),500


@app.route('/<table>/<int:id>', methods=['PUT'])
@require_api_key(['GET','POST'])
def update_row(table, id):
    allowed_tables = {"boats", "boats_2", "boats_3"}
    if table not in allowed_tables:
        return jsonify({'error': 'Invalid table name'}),400
    
    data2 = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM {table} WHERE id = %s", (id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error":"Row not found"}),404
    
    name = data2.get("name", row['name'])
    latitude = data2.get("latitude", row['latitude'])
    longitude = data2.get("longitude", row['longitude'])
    moving = data2.get("moving", row['moving'])

    cursor.execute(f"UPDATE {table} SET name=%s, latitude=%s, longitude=%s, moving=%s WHERE id=%s",
                   (name, latitude, longitude, moving, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message":"Row updated successfully"}),200

@app.route('/<table>', methods=['GET'])
@app.route('/<table>/<int:id>', methods=['GET'])
@require_api_key(['GET','POST'])
def get_data(table, id=None):
    allowed_tables = {"boats", "boats_2", "boats_3"}
    if table not in allowed_tables:
        return jsonify({'error': 'Invalid table name'}),400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if id is not None:
            cursor.execute(f"SELECT * FROM {table} WHERE id=%s",(id,))
            row = cursor.fetchone()
            if row:
                return jsonify(row),200
            else:
                return jsonify({"error":"Row not found"}),404
        else:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            return jsonify(rows),200
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
