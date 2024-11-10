from flask import Flask, request, jsonify

app = Flask(__name__)

# Example route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    # Example validation (replace with actual logic)
    if username == 'user' and password == 'pass' and role in ['Job Seeker', 'Business']:
        return jsonify({"success": True, "message": f"Welcome, {username}!"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
