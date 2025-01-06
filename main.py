from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route for the main page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the profile page
@app.route('/profile', methods=['GET'])
def profile():
    user_id = request.args.get('id')
    return render_template('profile.html', user_id=user_id)

# Route for the room page
@app.route('/room', methods=['GET'])
def room():
    room_id = request.args.get('id')
    if not room_id:
        return "Room ID is required", 400
    return render_template('room.html', room_id=room_id)

# API endpoints for room and profile events
@app.route('/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    return jsonify({"message": "Room created", "data": data})

@app.route('/join_room', methods=['POST'])
def join_room():
    data = request.get_json()
    return jsonify({"message": "Joined room", "data": data})

@app.route('/leave_room', methods=['POST'])
def leave_room():
    data = request.get_json()
    return jsonify({"message": "Left room", "data": data})

@app.route('/delete_room', methods=['POST'])
def delete_room():
    data = request.get_json()
    return jsonify({"message": "Room deleted", "data": data})

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    return jsonify({"message": "Profile updated", "data": data})

@app.route('/get_rooms', methods=['GET'])
def get_rooms():
    return jsonify({"rooms": ["Room1", "Room2", "Room3"]})

@app.route('/add_friend', methods=['POST'])
def add_friend():
    data = request.get_json()
    return jsonify({"message": "Friend added", "data": data})

@app.route('/delete_friend', methods=['POST'])
def delete_friend():
    data = request.get_json()
    return jsonify({"message": "Friend deleted", "data": data})

# Custom 404 handler
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
