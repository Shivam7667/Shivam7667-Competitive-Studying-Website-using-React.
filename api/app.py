# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_socketio import SocketIO, emit
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# import datetime
# import traceback

# # Initialize Flask app, CORS, Bcrypt, and SocketIO for real-time features
# app = Flask(__name__)
# CORS(app)
# bcrypt = Bcrypt(app)
# socketio = SocketIO(app)

# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017/')
# db = client['study_app']
# users = db['users']
# friend_requests = db['friend_requests']
# sessions = db['study_sessions']

# # Helper functions for MongoDB interactions
# def find_user_by_id(user_id):
#     return users.find_one({"_id": ObjectId(user_id)})

# def create_user(data):
#     result = users.insert_one(data)
#     return str(result.inserted_id)

# def update_user_study_time(user_id, study_time):
#     users.update_one({'_id': ObjectId(user_id)}, {'$set': {'study_time': study_time}})

# def get_leaderboard_by_category(category, user_id):
#     user = find_user_by_id(user_id)
#     if category == 'friends':
#         friend_ids = user.get('friends', [])
#         leaderboard = list(users.find({'_id': {'$in': friend_ids}}).sort('study_time', -1))
#     elif category == 'college':
#         college = user.get('college', '')
#         leaderboard = list(users.find({'college': college}).sort('study_time', -1))
#     elif category == 'city':
#         city = user.get('city', '')
#         leaderboard = list(users.find({'city': city}).sort('study_time', -1))
#     else:
#         return {"error": "Invalid category"}, 400
#     return leaderboard

# # --- Study Timer Management ---
# @app.route('/study/start', methods=['POST'])
# def start_study():
#     try:
#         data = request.json
#         if 'user_id' not in data:
#             return jsonify({"error": "user_id is required"}), 400

#         user_id = data['user_id']
#         start_time = datetime.datetime.now()

#         session_data = {
#             "user_id": ObjectId(user_id),
#             "start_time": start_time,
#             "end_time": None,
#             "duration": None
#         }
#         session_id = sessions.insert_one(session_data).inserted_id
#         return jsonify({"message": "Study session started", "session_id": str(session_id), "start_time": start_time}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error starting study session"}), 500

# @app.route('/study/stop', methods=['PUT'])
# def stop_study():
#     try:
#         data = request.json
#         if 'session_id' not in data:
#             return jsonify({"error": "session_id is required"}), 400

#         session_id = data['session_id']
#         end_time = datetime.datetime.now()

#         session = sessions.find_one({"_id": ObjectId(session_id)})
#         if not session:
#             return jsonify({"error": "Session not found"}), 404

#         duration = (end_time - session['start_time']).total_seconds()
#         sessions.update_one({"_id": ObjectId(session_id)}, {"$set": {"end_time": end_time, "duration": duration}})
#         update_user_study_time(session['user_id'], duration)

#         # Notify users with the updated leaderboard
#         leaderboard = list(users.find().sort('study_time', -1))
#         socketio.emit('update-leaderboard', leaderboard)

#         return jsonify({"message": "Study session stopped", "end_time": end_time, "duration": duration}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error stopping study session"}), 500

# @app.route('/study/history', methods=['GET'])
# def get_study_history():
#     try:
#         user_id = request.args.get('user_id')
#         if not user_id:
#             return jsonify({"error": "user_id is required"}), 400

#         sessions_history = list(sessions.find({"user_id": ObjectId(user_id)}))
#         return jsonify(sessions_history), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error retrieving study history"}), 500

# # --- Friend Management ---
# @app.route('/friends/request', methods=['POST'])
# def send_friend_request():
#     try:
#         data = request.json
#         if 'senderId' not in data or 'receiverEmail' not in data:
#             return jsonify({"error": "senderId and receiverEmail are required"}), 400

#         sender_id = data['senderId']
#         receiver_email = data['receiverEmail']

#         receiver = users.find_one({"email": receiver_email})
#         if not receiver:
#             return jsonify({"message": "User not found"}), 404

#         existing_request = friend_requests.find_one({
#             "sender": ObjectId(sender_id),
#             "receiver": receiver['_id'],
#             "status": "pending"
#         })
#         if existing_request:
#             return jsonify({"message": "Friend request already sent"}), 400

#         request_data = {
#             "sender": ObjectId(sender_id),
#             "receiver": receiver['_id'],
#             "status": "pending"
#         }
#         friend_requests.insert_one(request_data)
#         return jsonify({"message": "Friend request sent"}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error sending friend request"}), 500

# @app.route('/friends/request/accept', methods=['PUT'])
# def accept_friend_request():
#     try:
#         data = request.json
#         if 'requestId' not in data:
#             return jsonify({"error": "requestId is required"}), 400

#         request_id = data['requestId']
#         friend_requests.update_one({"_id": ObjectId(request_id)}, {"$set": {"status": "accepted"}})

#         friend_request = friend_requests.find_one({"_id": ObjectId(request_id)})
#         if friend_request:
#             users.update_one({"_id": friend_request['sender']}, {"$addToSet": {"friends": friend_request['receiver']}})
#             users.update_one({"_id": friend_request['receiver']}, {"$addToSet": {"friends": friend_request['sender']}})
#         return jsonify({"message": "Friend request accepted"}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error accepting friend request"}), 500

# @app.route('/friends/request/reject', methods=['PUT'])
# def reject_friend_request():
#     try:
#         data = request.json
#         if 'requestId' not in data:
#             return jsonify({"error": "requestId is required"}), 400

#         request_id = data['requestId']
#         friend_requests.update_one({"_id": ObjectId(request_id)}, {"$set": {"status": "rejected"}})
#         return jsonify({"message": "Friend request rejected"}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error rejecting friend request"}), 500

# @app.route('/friends/list/<user_id>', methods=['GET'])
# def get_friends(user_id):
#     try:
#         friends = find_user_by_id(user_id).get('friends', [])
#         friends_list = list(users.find({"_id": {"$in": friends}}))
#         return jsonify(friends_list), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error retrieving friends list"}), 500

# @app.route('/friends/requests/<user_id>', methods=['GET'])
# def pending_requests(user_id):
#     try:
#         requests = list(friend_requests.find({"receiver": ObjectId(user_id), "status": "pending"}))
#         return jsonify(requests), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error retrieving friend requests"}), 500

# # --- Leaderboard ---
# @app.route('/leaderboard/<category>', methods=['GET'])
# def get_leaderboard(category):
#     try:
#         user_id = request.args.get('user_id')
#         if not user_id:
#             return jsonify({"error": "user_id is required"}), 400

#         leaderboard = get_leaderboard_by_category(category, user_id)
#         return jsonify(leaderboard), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error retrieving leaderboard"}), 500

# # --- Authentication ---
# @app.route('/api/signup', methods=['POST'])
# def signup():
#     try:
#         data = request.json
#         email = data.get('email')
#         password = data.get('password')

#         if users.find_one({'email': email}):
#             return jsonify({'error': 'Email already exists'}), 400

#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         user_id = users.insert_one({
#             'email': email,
#             'password': hashed_password,
#             'friends': [],
#             'study_time': 0
#         }).inserted_id
#         return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error creating user"}), 500

# @app.route('/api/signin', methods=['POST'])
# def signin():
#     try:
#         data = request.json
#         email = data.get('email')
#         password = data.get('password')

#         user = users.find_one({'email': email})
#         if not user or not bcrypt.check_password_hash(user['password'], password):
#             return jsonify({'error': 'Invalid credentials'}), 400

#         return jsonify({'message': 'Login successful', 'user_id': str(user['_id'])}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()
#         return jsonify({"error": "Error logging in"}), 500

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
# app.py
# app.py
# app.py
# app.py
# app.py
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

# Importing the Blueprints
from auth import auth_bp  # Import the auth Blueprint
from friend import friend_bp  # Import the friend Blueprint
from study_routes import study_hp, init_app  # Import the new study Blueprint and init_app function

# Initialize Flask app
app = Flask(__name__)

# Set up CORS for cross-origin requests
CORS(app)

# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/study_app_db'  # Change to your MongoDB URI
mongo = PyMongo(app)

# Initialize Bcrypt with the Flask app for password hashing
bcrypt = Bcrypt(app)

# Initialize the study routes with the mongo instance
init_app(mongo)

# Register the Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(friend_bp)
app.register_blueprint(study_hp)  # Register the study Blueprint

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask application

