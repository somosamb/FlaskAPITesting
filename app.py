# app.py

from flask import Flask, request, jsonify, make_response, abort
import os
import json

# Create the Flask app instance
app = Flask(__name__)

# Define the path where user data will be saved
DATA_FILE = "users.json"

# Create an empty dictionary to hold the user data
users = {}

# -------------------------------
# Utility: Load users from file
# -------------------------------
def load_users():
    global users
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}  # If file is corrupt or empty
    else:
        users = {}

# -------------------------------
# Utility: Save users to file
# -------------------------------
def save_users():
    with open(DATA_FILE, "w") as file:
        json.dump(users, file, indent=2)

# -------------------------------
# Utility: Validate user payload
# -------------------------------
def validate_user_data(data):
    if not data:
        abort(make_response(jsonify({"error": "Missing JSON body"}), 400))
    if "name" not in data:
        abort(make_response(jsonify({"error": "Missing 'name' field"}), 400))
    if not isinstance(data["name"], str) or not data["name"].strip():
        abort(make_response(jsonify({"error": "'name' must be a non-empty string"}), 400))

# -------------------------------
# GET /users - List all users
# -------------------------------
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# -------------------------------
# GET /users/<id> - Retrieve user by ID
# -------------------------------
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        abort(make_response(jsonify({"error": "User not found"}), 404))
    # Correct response for test_get_user
    return jsonify({
        "user_id": user_id,
        "name": users[user_id]["name"]
    }), 200


# -------------------------------
# POST /users - Create new user
# -------------------------------
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    validate_user_data(data)

    # Generate a new unique ID
    if users:
        new_id = str(max(int(uid) for uid in users.keys()) + 1)
    else:
        new_id = "1"

    # Save the new user
    users[new_id] = {"name": data["name"]}
    save_users()

    # Correct response for test_create_user
    return jsonify({
        "user_id": str(new_id),
        "user": {"name": data["name"]}
    }), 201


# -------------------------------
# PUT /users/<id> - Upsert user
# -------------------------------
@app.route('/users/<user_id>', methods=['PUT'])
def upsert_user(user_id):
    data = request.get_json()
    validate_user_data(data)

    # Check whether the user exists before update
    is_new = user_id not in users

    # Upsert the user
    users[user_id] = {"name": data["name"]}
    save_users()

    # Prepare the full response payload with user info
    response_data = {
        "message": "User created" if is_new else "User updated",
        "user": users[user_id]
    }

    # Send proper status code and headers
    status_code = 201 if is_new else 200
    response = make_response(jsonify(response_data), status_code)
    response.headers["Location"] = f"/users/{user_id}"
    return response


# -------------------------------
# DELETE /users/<id> - Delete a user
# -------------------------------
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        save_users()
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# -------------------------------
# App Entry Point
# -------------------------------
if __name__ == '__main__':
    # Load users when app starts
    load_users()

    # Run the Flask app on localhost port 5000
    app.run(debug=True)
