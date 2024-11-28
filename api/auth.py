from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import traceback

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client['ecommerce_db']
users = db['users']

# Initialize Bcrypt instance
bcrypt = Bcrypt()

# --- Authentication ---
@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        if users.find_one({'email': email}):
            return jsonify({'error': 'Email already exists'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = users.insert_one({
            'email': email,
            'password': hashed_password,
            'friends': [],
            'study_time': 0
        }).inserted_id

        return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": "Error creating user"}), 500

@auth_bp.route('/api/signin', methods=['POST'])
def signin():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = users.find_one({'email': email})
        if not user or not bcrypt.check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid credentials'}), 400

        return jsonify({'message': 'Login successful', 'user_id': str(user['_id'])}), 200
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": "Error logging in"}), 500
