# 🔐 End-to-End Encrypted Real-Time Chat Application

A browser-based, end-to-end encrypted, real-time chat application built with Flask and WebSockets. All communication is handled in-memory without any database, ensuring privacy and fast performance.

---

## ✨ Features

- ✨ **Animated Landing Page** - Beautiful, engaging landing page with smooth animations
- 🔐 **End-to-End Encryption** - Messages are encrypted using Fernet symmetric encryption
- ⚡ **Real-Time Messaging** - Instant message delivery using WebSocket technology
- 👥 **Multi-User Support** - Multiple users can chat simultaneously in rooms
- 🎨 **Emoji Avatars** - Choose from 20+ emoji avatars to personalize your profile
- 🌙 **Dark Mode** - Toggle between light and dark themes for better usability
- ⌨️ **Typing Indicators** - See when others are typing, just like WhatsApp/Telegram
- 📊 **Live User List** - Real-time display of online users with total count
- 💬 **System Messages** - Automatic notifications when users join or leave
- 📋 **Room ID Sharing** - Easy-to-copy room IDs for inviting others
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices

---

## ⚒️ Technology Stack

- **Backend**: Flask (Python)
- **Real-Time Communication**: Flask-SocketIO (WebSockets)
- **Encryption**: Cryptography (Fernet symmetric encryption)
- **Frontend**: HTML5, CSS3, JavaScript
- **Storage**: In-memory (no database required)

---

## 📩 Installation (local)

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

---

## 🚀 Deployment (Free Hosting on Render)
You can deploy this app online for free using [Render](https://render.com)

### Step 1: Prepare Your Project
- **Ensure you have these files in the root directory:**
   - `app.py`
   - `requirements.txt`
   - `Procfile`

- **Example `requirements.txt`:**
```bash
flask
flask-socketio
cryptography
gunicorn
eventlet

```
- **Example `Procfile`:**
```txt
web: gunicorn --worker-class eventlet -w 1 app:app
```

### Step 2: Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/Browser-based-chat-application.git
git push -u origin main
```

### Step 3: Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub and authorize access to your repo

### Step 4: Deploy Web Service
1. Click New + → Web Service
2. Select your GitHub repo
3. Configure:
   - **Environment:** Python 3.x
   - Build Command:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     gunicorn --worker-class eventlet -w 1 app:app
     ```
     
   - **Instance Type: Free**

4. Click Create/Deploy Web Service

### Step 5: Access Your App
- Render will give you a public URL like:
```Code
https://your-app-name.onrender.com
```
- Open it in your browser and start chatting 🎉

---

## 📱 Run on Mobile (Local Network)  
You can also use the application on your mobile phone without deploying it online, as long as your phone and computer are connected to the same Wi‑Fi network.

### Steps:
1. **Find your system’s local IP address**
   - **On Windows:**  
      Open Command Prompt and run:
     ```bash
     ipconfig
     ```  
      Look for the `IPv4 Address` (e.g., `192.168.1.5`).  
   - **On macOS/Linux:**  
      Open Terminal and run:
     ```bash
     ifconfig
     ```
     Look for the `inet` address under your active network (e.g., `192.168.1.5`).

2. **Run the Flask app**
   ```bash
   python app.py
   ```  
3. **Access from your mobile browser**
   - On your phone, open a browser and type:  
     ```Code  
     http://<your-system-ip>:5000  
     ```
     Example:
     ```Code
     http://192.168.1.5:5000
     ```
4. **Start chatting**  
- You’ll see the same landing page on your mobile.
- Create or join rooms and chat in real time, just like on desktop.

### ⚠️ Notes  
- Both devices must be on the **same Wi‑Fi network.**
- This works only while the Flask server is running on your computer.
- No internet deployment is required — everything stays local.

---

## 🌐 Live Demo
You can try the application directly here:  
👉 Encrypted Chat App on Render [Click Here](https://browser-based-chat-application.onrender.com)

---

## 📸 Screenshots

**1. Landing Page**

<img width="1917" height="1098" alt="Landing Page" src="https://github.com/user-attachments/assets/5c8aac00-af0c-4751-b6f7-cc8957d5a906" />

**2. Create Room**
<img width="1917" height="1096" alt="Create Rooom" src="https://github.com/user-attachments/assets/540fdbef-4622-4476-9de6-90a437f1a11f" />
<img width="1919" height="1094" alt="Created Room" src="https://github.com/user-attachments/assets/f46bdb05-aa69-442d-9db5-52b8361b99bc" />


**3. Join Room**
<img width="1916" height="1108" alt="Join Room" src="https://github.com/user-attachments/assets/defe8f27-cca3-417a-bd71-a6f6004c3c11" />
<img width="1919" height="1094" alt="Joined room" src="https://github.com/user-attachments/assets/919b38d7-6199-48a9-a650-db3a6c5ceeb2" />

---

## 📝 Usage

### Creating a Room

1. Click **"Create a Room"** on the landing page
2. Enter your username
3. Select an emoji avatar
4. Click **"Create Room & Enter Chat"**
5. Share the generated Room ID with others to invite them

### Joining a Room

1. Click **"Join a Chat"** on the landing page
2. Enter the Room ID provided by the room creator
3. Enter your username
4. Select an emoji avatar
5. Click **"Join Chat Room"**

### Chatting

- **Send Messages**: Type your message and press Enter or click Send
- **Copy Room ID**: Click the 📋 button to copy the room ID
- **Toggle Dark Mode**: Click the 🌙/☀️ button to switch themes
- **Leave Chat**: Click the 🚪 button to return to the landing page

---

## 🔐 Security Features

- **End-to-End Encryption**: All messages are encrypted using Fernet encryption before storage
- **In-Memory Storage**: No persistent database - data exists only during active sessions
- **Room-Based Encryption**: Each room has its own unique encryption key
- **Secure Key Sharing**: Encryption keys are shared securely with room members via WebSocket

---

## 🎯 Architecture

### In-Memory Data Structure

- **Rooms**: Dictionary storing room data, users, messages, and encryption keys
- **User Sessions**: Dictionary mapping WebSocket sessions to user information
- **Messages**: Stored encrypted in memory (last 100 messages per room)

### WebSocket Events

- `join_chat`: User joins a chat room
- `send_message`: User sends a message
- `typing`: Typing indicator events
- `new_message`: Broadcast new message to all room members
- `user_joined`: Notify when a user joins
- `user_left`: Notify when a user leaves
- `user_list_update`: Update online user list
- `user_typing`: Show/hide typing indicator

---

## 📂 Project Structure

```
├── app.py                  # Main Flask application with WebSocket handlers
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Landing page
│   ├── create_room.html  # Create room page
│   ├── join_room.html    # Join room page
│   └── chat.html         # Chat room interface
└── static/               # Static files
    ├── css/
    │   └── style.css     # All styles including animations
    └── js/
        └── chat.js       # Client-side JavaScript for chat functionality
```

---

## Performance Optimizations

- **Message Limit**: Only last 100 messages stored per room
- **Message History**: Only last 50 messages sent to new users
- **Efficient WebSocket**: Event-driven architecture for low latency
- **Client-Side Rendering**: Smooth UI updates without page refreshes

---

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

---

## Limitations

- **No Persistent Storage**: All data is lost when the server restarts
- **No User Authentication**: Users can use any username
- **Single Server**: Not designed for horizontal scaling
- **Memory Based**: Limited by available server memory

---

## 💡 Future Enhancements

- [ ] File sharing support
- [ ] Message reactions
- [ ] User profiles
- [ ] Message search
- [ ] Persistent storage option
- [ ] Multi-server support
- [ ] Voice/video chat integration

---

## 📜 License

This project is open source and available for educational and personal use.

---
## 💛 Contributing

Feel free to fork this project and submit pull requests for any improvements!

---
## Support

For issues or questions, please open an issue on the repository.

---

**Note**: This application is designed for demonstration and educational purposes. For production use, additional security measures, authentication, and persistence layers should be implemented.
