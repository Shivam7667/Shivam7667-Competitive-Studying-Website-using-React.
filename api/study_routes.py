from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
from datetime import datetime
import pytz
from bson.objectid import ObjectId  # Import ObjectId for MongoDB

# Create a Blueprint for study routes
study_hp = Blueprint('study', __name__)

# Timezone
IST = pytz.timezone('Asia/Kolkata')

# MongoDB Configuration
mongo = None  # Initialize mongo as None

def set_mongo(mongo_instance):
    global mongo
    mongo = mongo_instance

# Study Routes
@study_hp.route('/study/start', methods=['POST'])
def start_study_session():
    user_id = request.json.get('user_id')
    start_time = datetime.now(IST)  # Get the current time in IST
    session_id = str(mongo.db.study_sessions.insert_one({
        'user_id': user_id,
        'start_time': start_time,
        'end_time': None
    }).inserted_id)
    return jsonify({'session_id': session_id, 'start_time': start_time.isoformat()}), 201

@study_hp.route('/study/stop', methods=['PUT'])
def stop_study_session():
    session_id = request.json.get('session_id')
    end_time = datetime.now(IST)  # Get the current time in IST
    mongo.db.study_sessions.update_one(
        {'_id': ObjectId(session_id)},  # Ensure session_id is an ObjectId
        {'$set': {'end_time': end_time}}
    )
    return jsonify({'message': 'Session updated successfully', 'end_time': end_time.isoformat()}), 200

@study_hp.route('/study/history', methods=['GET'])
def get_study_history():
    user_id = request.args.get('user_id')
    history = mongo.db.study_sessions.find({'user_id': user_id})

    return jsonify([{
        'session_id': str(session['_id']),
        'start_time': session['start_time'].isoformat(),
        'end_time': session['end_time'].isoformat() if session['end_time'] else None,
        'duration_hours': (session['end_time'] - session['start_time']).total_seconds() / 3600 if session['end_time'] else None
    } for session in history]), 200

# Set the MongoDB instance
def init_app(mongo_instance):
    set_mongo(mongo_instance)
