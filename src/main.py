from flask import Flask, render_template, request, jsonify, redirect, url_for

from src.handler import AuthHandler, UserAdapter
from src.model.AuthData import AuthData
from src.model.User import User

app = Flask(__name__)


# Route for the main page
@app.route('/')
def home():
    return render_template('home.html')


# Route for the profile page
@app.route('/profile', methods=['GET'])
def profile():
    user_id = request.args.get('id')
    user = UserAdapter.get_user(user_id)
    friends = user.friends
    return render_template('profile.html', user=user, friends=friends)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Переменная для ошибки
    join = request.args.get('join')
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form['username']
        password = request.form['password']
        # Логика для проверки данных

        if AuthHandler.auth(AuthData(username, password)):
            return redirect('/profile')  # Перенаправление на страницу приветствия
        else:
            error = 'Неверные данные. Попробуйте снова.'  # Устанавливаем ошибку

    # Если запрос GET или ошибка в POST, отображаем форму
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET, POST'])
def register():
    user_id = request.args.get('id')
    return render_template('src/register.html', user_id=user_id)


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


@app.route('/join_room', methods=['GET'])
def join_room():
    code = request.args.get('code')
    room_id = UserAdapter.joinRoom(code)
    if room_id:
        return redirect(url_for('room', room_id=room_id))
    return redirect(url_for('profile', error=1))


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
    return render_template('PageNotFound.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
