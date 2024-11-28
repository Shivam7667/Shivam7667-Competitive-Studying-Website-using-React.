from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime

# Create a Blueprint for study-related routes
study_bp = Blueprint('study', __name__)

# Global mongo instance
mongo = None

def set_mongo(mongo_instance):
    global mongo
    mongo = mongo_instance

# Route to start a study session
@study_bp.route('/study/start', methods=['POST'])
def start_study_session():
    try:
        # Create a new study session with the current timestamp
        session_data = {
            "start_time": datetime.utcnow(),
            "end_time": None,  # Will be updated when the session is stopped
            "duration": None  # To be calculated when the session is stopped
        }
        result = mongo.db.study_sessions.insert_one(session_data)
        return jsonify({"session_id": str(result.inserted_id)}), 201
    except Exception as e:
        print(f"Error occurred while starting session: {e}")
        return jsonify({"error": "Failed to start study session"}), 500

# Route to stop a study session
@study_bp.route('/study/stop', methods=['PUT'])
def stop_study_session():
    try:
        # Retrieve session_id from the request body
        session_id = request.json.get('session_id')
        if not session_id:
            return jsonify({"error": "Session ID is required"}), 400

        # Fetch the session from MongoDB using the session_id
        session = mongo.db.study_sessions.find_one({"_id": ObjectId(session_id)})
        if not session:
            return jsonify({"error": "Session not found"}), 404
        if session["end_time"] is not None:
            return jsonify({"error": "Session already stopped"}), 400

        # Calculate the session duration
        end_time = datetime.utcnow()
        duration = (end_time - session["start_time"]).total_seconds()

        # Update the session in the database
        mongo.db.study_sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"end_time": end_time, "duration": duration}}
        )
        return jsonify({"message": "Session stopped successfully", "duration": duration}), 200
    except Exception as e:
        print(f"Error occurred while stopping session: {e}")
        return jsonify({"error": "Failed to stop study session"}), 500

# Route to fetch study session history
@study_bp.route('/study/history', methods=['GET'])
def get_study_history():
    try:
        # Fetch all sessions that have been completed (i.e., have an end_time)
        sessions = mongo.db.study_sessions.find({"end_time": {"$ne": None}})
        history = [
            {
                "id": str(session["_id"]),
                "start_time": session["start_time"],
                "end_time": session["end_time"],
                "duration": session["duration"]
            }
            for session in sessions
        ]
        return jsonify(history), 200
    except Exception as e:
        print(f"Error occurred while fetching study history: {e}")
        return jsonify({"error": "Failed to retrieve study history"}), 500

# Route to fetch study materials (mock materials)
@study_bp.route('/study/materials', methods=['GET'])
def get_study_materials():
    try:
        # Simulating some study materials
        materials = [
            {"title": "React for Beginners", "url": "https://reactjs.org/docs/getting-started.html"},
            {"title": "Flask Documentation", "url": "https://flask.palletsprojects.com/en/latest/"},
            {"title": "MongoDB Basics", "url": "https://docs.mongodb.com/manual/tutorial/getting-started/"}
        ]
        return jsonify(materials), 200
    except Exception as e:
        print(f"Error occurred while fetching study materials: {e}")
        return jsonify({"error": "Failed to retrieve study materials"}), 500

# Function to set the mongo instance
def init_app(mongo_instance):
    set_mongo(mongo_instance)
