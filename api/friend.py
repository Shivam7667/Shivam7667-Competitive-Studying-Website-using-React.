from flask import Blueprint, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint for friends
friend_bp = Blueprint('friend', __name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client['ecommerce_db']
users = db['users']

# Allow CORS for this blueprint
CORS(friend_bp)

# Fetch Friends List
@friend_bp.route('/list/<user_id>', methods=['GET'])
@jwt_required()  # Require a valid JWT token to access this route
def get_friends_list(user_id):
    # Fetch user from the database
    user = users.find_one({"_id": ObjectId(user_id)})
    if user:
        friends_list = user.get('friends', [])
        # Fetch friend details
        friends_details = []
        for friend_id in friends_list:
            friend = users.find_one({"_id": ObjectId(friend_id)})
            if friend:
                friends_details.append({"_id": str(friend['_id']), "name": friend['email']})  # Modify as needed
        return jsonify(friends_details), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Fetch Pending Friend Requests
@friend_bp.route('/requests/<user_id>', methods=['GET'])
@jwt_required()  # Require a valid JWT token to access this route
def get_pending_requests(user_id):
    user = users.find_one({"_id": ObjectId(user_id)})
    if user:
        pending_requests = user.get('pending_requests', [])
        return jsonify({"pending_requests": pending_requests}), 200
    else:
        return jsonify({"error": "User not found"}), 404
