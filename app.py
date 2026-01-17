from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid
import secrets
from datetime import datetime
from cryptography.fernet import Fernet
import base64
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory data storage
rooms = {}  # {room_id: {'users': {}, 'messages': []}}
user_sessions = {}  # {session_id: {'username': str, 'room_id': str, 'avatar': str}}

def generate_room_id():
    """Generate a unique room ID"""
    return str(uuid.uuid4())[:8].upper()

def generate_encryption_key():
    """Generate encryption key for a room"""
    return Fernet.generate_key()

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/create-room', methods=['GET'])
def create_room():
    """Page to create a new room"""
    return render_template('create_room.html')

@app.route('/join-room', methods=['GET'])
def join_room_page():
    """Page to join an existing room"""
    return render_template('join_room.html')

@app.route('/chat', methods=['GET'])
def chat():
    """Chat room page"""
    room_id = request.args.get('room_id', '').upper()
    username = request.args.get('username', '')
    avatar = request.args.get('avatar', '')
    
    if not room_id or not username or not avatar:
        return render_template('index.html'), 302
    
    # Verify room exists
    if room_id not in rooms:
        return render_template('index.html'), 302
    
    return render_template('chat.html', 
                         room_id=room_id, 
                         username=username, 
                         avatar=avatar)

@app.route('/api/create-room', methods=['POST'])
def api_create_room():
    """API endpoint to create a new room"""
    data = request.json
    username = data.get('username', '').strip()
    avatar = data.get('avatar', '')
    
    if not username or not avatar:
        return jsonify({'error': 'Username and avatar are required'}), 400
    
    room_id = generate_room_id()
    encryption_key = generate_encryption_key()
    
    rooms[room_id] = {
        'users': {},
        'messages': [],
        'encryption_key': encryption_key
    }
    
    return jsonify({
        'room_id': room_id,
        'username': username,
        'avatar': avatar
    })

@app.route('/api/verify-room', methods=['POST'])
def api_verify_room():
    """API endpoint to verify if a room exists"""
    data = request.json
    room_id = data.get('room_id', '').strip().upper()
    
    if room_id in rooms:
        return jsonify({'exists': True})
    return jsonify({'exists': False}), 404

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    session_id = request.sid
    if session_id in user_sessions:
        user_data = user_sessions[session_id]
        room_id = user_data.get('room_id')
        username = user_data.get('username')
        
        if room_id and room_id in rooms:
            # Remove user from room
            rooms[room_id]['users'].pop(session_id, None)
            leave_room(room_id)
            
            # Notify others
            socketio.emit('user_left', {
                'username': username,
                'timestamp': datetime.now().strftime('%H:%M')
            }, room=room_id)
            
            socketio.emit('user_list_update', {
                'users': list(rooms[room_id]['users'].values()),
                'count': len(rooms[room_id]['users'])
            }, room=room_id)
        
        del user_sessions[session_id]
    print(f'Client disconnected: {request.sid}')

@socketio.on('join_chat')
def handle_join_chat(data):
    """Handle user joining a chat room"""
    room_id = data.get('room_id', '').upper()
    username = data.get('username', '').strip()
    avatar = data.get('avatar', '')
    session_id = request.sid
    
    if not room_id or room_id not in rooms:
        emit('error', {'message': 'Invalid room ID'})
        return
    
    if not username or not avatar:
        emit('error', {'message': 'Username and avatar are required'})
        return
    
    # Store user session
    user_sessions[session_id] = {
        'username': username,
        'room_id': room_id,
        'avatar': avatar
    }
    
    # Add user to room
    rooms[room_id]['users'][session_id] = {
        'username': username,
        'avatar': avatar
    }
    
    # Join WebSocket room
    join_room(room_id)
    
    # Send encryption key and previous messages to new user
    # In a production system, this key would be shared through a secure channel
    # For this in-memory implementation, the key is shared with room members
    emit('room_key', {
        'encryption_key': base64.urlsafe_b64encode(rooms[room_id]['encryption_key']).decode()
    })
    
    # Decrypt messages for display (they remain encrypted in storage)
    fernet = Fernet(rooms[room_id]['encryption_key'])
    decrypted_messages = []
    for msg in rooms[room_id]['messages'][-50:]:
        try:
            if msg.get('is_encrypted'):
                decrypted_text = fernet.decrypt(msg['message'].encode()).decode()
            else:
                decrypted_text = msg['message']
        except:
            decrypted_text = msg['message']
        decrypted_messages.append({
            'username': msg['username'],
            'avatar': msg['avatar'],
            'message': decrypted_text,
            'timestamp': msg['timestamp'],
            'is_encrypted': True
        })
    
    emit('message_history', {
        'messages': decrypted_messages
    })
    
    # Notify others
    socketio.emit('user_joined', {
        'username': username,
        'avatar': avatar,
        'timestamp': datetime.now().strftime('%H:%M')
    }, room=room_id, include_self=False)
    
    # Update user list for everyone
    socketio.emit('user_list_update', {
        'users': list(rooms[room_id]['users'].values()),
        'count': len(rooms[room_id]['users'])
    }, room=room_id)
    
    emit('joined_successfully')

@socketio.on('send_message')
def handle_send_message(data):
    """Handle incoming message"""
    session_id = request.sid
    if session_id not in user_sessions:
        emit('error', {'message': 'Not authenticated'})
        return
    
    user_data = user_sessions[session_id]
    room_id = user_data['room_id']
    message_text = data.get('message', '').strip()
    
    if not message_text or room_id not in rooms:
        return
    
    # Encrypt message
    try:
        fernet = Fernet(rooms[room_id]['encryption_key'])
        encrypted_message = fernet.encrypt(message_text.encode()).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        encrypted_message = message_text
    
    # Store encrypted message
    stored_message = {
        'username': user_data['username'],
        'avatar': user_data['avatar'],
        'message': encrypted_message,
        'timestamp': datetime.now().strftime('%H:%M'),
        'is_encrypted': True
    }
    rooms[room_id]['messages'].append(stored_message)
    
    # Keep only last 100 messages
    if len(rooms[room_id]['messages']) > 100:
        rooms[room_id]['messages'] = rooms[room_id]['messages'][-100:]
    
    # Send decrypted message for display (stored version remains encrypted)
    message_data = {
        'username': user_data['username'],
        'avatar': user_data['avatar'],
        'message': message_text,  # Decrypted for display
        'timestamp': datetime.now().strftime('%H:%M'),
        'is_encrypted': True
    }
    
    # Broadcast to room
    socketio.emit('new_message', message_data, room=room_id)

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    session_id = request.sid
    if session_id not in user_sessions:
        return
    
    user_data = user_sessions[session_id]
    room_id = user_data['room_id']
    is_typing = data.get('is_typing', False)
    
    socketio.emit('user_typing', {
        'username': user_data['username'],
        'avatar': user_data['avatar'],
        'is_typing': is_typing
    }, room=room_id, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host= '0.0.0.0', debug=True, port=5000)
