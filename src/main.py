import os

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room
from werkzeug.utils import secure_filename

from src.handler.AuthHandler import AuthHandler
from src.handler.RoomAdapter import RoomAdapter
from src.handler.UserAdapter import UserAdapter
from src.model.AuthData import AuthData

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
socketio = SocketIO(app)

UPLOAD_FOLDER = 'src/static/sprites/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Разрешенные расширения файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Убедимся, что папка существует
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Проверка, разрешено ли расширение файла"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_sprite', methods=['POST'])
def upload_sprite():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Файл не найден'}), 400
    file = request.files['file']
    character_id = request.form.get('character_id')

    if not character_id:
        return jsonify({'success': False, 'message': 'Не указан ID персонажа'}), 400

    if file and allowed_file(file.filename):
        # Сохраняем файл с безопасным именем
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_url = f'/static/sprites/{filename}'
        sprite = roomAdapter.addSprite(session.get("room_id"), character_id, file_url)
        sprite["success"] = True
        characters_dict = roomAdapter.get_characters(session.get("room_id"))
        socketio.emit('characters_update', characters_dict, room=session.get("room_id"))
        return jsonify(sprite), 200
    else:
        return jsonify({'success': False, 'message': 'Неподдерживаемый формат файла'}), 400


@socketio.on("delete_sprite")
def delete_sprite(data):
    room_id = session.get('room_id')
    roomAdapter.delete_sprite(room_id, data)
    emit('state_updated', roomAdapter.get_current(room_id), room=room_id)
    characters_dict = roomAdapter.get_characters(room_id)
    emit('characters_update', characters_dict, room=room_id)


# Route for the main page
@app.route('/')
def home():
    return render_template('home.html')


# Route for the profile page
@app.route('/profile', methods=['GET'])
def profile():
    user_id = request.args.get('id')
    if user_id is None:
        user_id = session.get('user_id')
    user = userAdapter.get_user(user_id)
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

        if authHandler.auth(AuthData(username, password)):
            return redirect('/profile')  # Перенаправление на страницу приветствия
        else:
            error = 'Неверные данные. Попробуйте снова.'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET, POST'])
def register():
    user_id = request.args.get('id')
    return render_template('src/register.html', user_id=user_id)


# Route for the room page
@app.route('/room_page', methods=['GET'])
def room_page():
    room_id = int(request.args.get('room_id'))
    if not room_id:
        return "Room ID is required", 400
    room_data = roomAdapter.get_room(room_id)
    if not room_data:
        return "Room ID is invalid", 400
    if room_data.master_id == session.get('user_id'):
        return render_template('room_master.html', room=room_data)
    return render_template('room_player.html', room=room_data)


@socketio.on("new_character")
def new_character():
    room_id = session.get('room_id')
    roomAdapter.addCharacter(room_id)
    characters_dict = roomAdapter.get_characters(room_id)
    emit('characters_update', characters_dict, room=room_id)


@socketio.on('update_state')
def update_state(data):
    room_id = session.get("room_id")
    data = roomAdapter.updateRoom(room_id, data)
    emit('state_updated', data, room=room_id)


# API endpoints for room and profile events
@app.route('/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    return jsonify({"message": "Room created", "data": data})


@app.route('/join_room', methods=['GET'])
def join():
    code = request.args.get('code')
    room_id = userAdapter.joinRoom(code, session.get('user_id'))
    session['room_id'] = room_id
    print(session.get('user_id'), session.get('room_id'))
    if room_id:
        return redirect(url_for('room_page', room_id=room_id))
    return redirect(url_for('profile', error=1))


@socketio.on('connect')
def handle_connect():
    print("aidaho")
    room_id = session.get('room_id')
    if room_id:
        join_room(room_id)
        emit('joined_room', {'status': 'success', 'room_id': room_id})
        emit('state_updated', {"current_background": roomAdapter.get_room(room_id).current_background}, room=room_id)
        emit('state_updated', roomAdapter.get_current(room_id), room=room_id)
        characters_dict = roomAdapter.get_characters(room_id)
        emit('characters_update', characters_dict, room=room_id)
    else:
        emit('error', {'status': 'failure', 'message': 'No room assigned'})


@socketio.on('leave_room')
def handle_leave():
    leave_room(session.get('room_id'))


@socketio.on("delete_current")
def delete_current(data):
    room_id = session.get('room_id')
    roomAdapter.remove_current(room_id, data)
    emit('delete_current_ans', data, room=room_id)

@socketio.on("character_delete")
def character_delete(data):
    room_id = session.get('room_id')
    roomAdapter.delete_character(room_id, data['characterId'])
    emit('characters_update', roomAdapter.get_characters(room_id), room=room_id)


@socketio.on("character_update")
def character_update(data):
    room_id = session.get('room_id')
    roomAdapter.updateCharacter(room_id, data['characterId'], data['name'])
    emit('characters_update', roomAdapter.get_characters(room_id), room=room_id)


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
    userAdapter = UserAdapter()
    authHandler = AuthHandler(session=session)
    roomAdapter = RoomAdapter()
    app.run(debug=True)
