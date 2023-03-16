import json
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)

# Load the existing user data from the JSON file
with open('users.json', 'r') as f:
    users = json.load(f)

# User authentication routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username in users:
        return jsonify({'message': 'Username already taken'}), 400
    users[username] = password
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username not in users:
        return jsonify({'message': 'User not found'}), 404
    if users[username] != password:
        return jsonify({'message': 'Incorrect password'}), 401
    session['username'] = username
    return jsonify({'message': 'Login successful'})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'})

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'verysecretkey' # Add a secret key for session management
    app.run(debug=True)
