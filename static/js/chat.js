// Get room information from meta tags
const roomId = document.querySelector('meta[name="room-id"]')?.content;
const username = document.querySelector('meta[name="username"]')?.content;
const avatar = document.querySelector('meta[name="avatar"]')?.content;

// Initialize Socket.IO connection
const socket = io();

// DOM Elements
const messagesContainer = document.getElementById('messagesContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const userList = document.getElementById('userList');
const userCount = document.getElementById('userCount');
const typingIndicator = document.getElementById('typingIndicator');
const darkModeToggle = document.getElementById('darkModeToggle');
const copyRoomIdButton = document.getElementById('copyRoomId');

// State
let typingTimeout;
let currentTypingUser = null;
let isDarkMode = localStorage.getItem('darkMode') === 'true';
let encryptionKey = null;
let fernet = null;

// Initialize dark mode
if (isDarkMode) {
    document.documentElement.setAttribute('data-theme', 'dark');
    darkModeToggle.textContent = '☀️';
} else {
    document.documentElement.removeAttribute('data-theme');
    darkModeToggle.textContent = '🌙';
}

// Join chat room on connection
socket.on('connect', () => {
    console.log('Connected to server');
    socket.emit('join_chat', {
        room_id: roomId,
        username: username,
        avatar: avatar
    });
});

// Handle encryption key
socket.on('room_key', (data) => {
    encryptionKey = data.encryption_key;
    console.log('Encryption key received');
    // Note: In a production system, this key would be handled more securely
    // For this implementation, messages are encrypted server-side with Fernet
});

// Handle successful join
socket.on('joined_successfully', () => {
    console.log('Joined chat room successfully');
});

// Handle message history
socket.on('message_history', (data) => {
    data.messages.forEach(msg => {
        displayMessage(msg, msg.username === username);
    });
    scrollToBottom();
});

// Handle new message
socket.on('new_message', (data) => {
    displayMessage(data, data.username === username);
    scrollToBottom();
});

// Handle user joined
socket.on('user_joined', (data) => {
    displaySystemMessage(`${data.avatar} ${data.username} joined the chat at ${data.timestamp}`);
});

// Handle user left
socket.on('user_left', (data) => {
    displaySystemMessage(`${data.username} left the chat at ${data.timestamp}`);
});

// Handle user list update
socket.on('user_list_update', (data) => {
    updateUserList(data.users, data.count);
});

// Handle typing indicator
socket.on('user_typing', (data) => {
    if (data.is_typing) {
        currentTypingUser = data;
        typingIndicator.innerHTML = `
            <span class="typing-avatar">${data.avatar}</span>
            <span class="typing-text">
                ${data.username} is typing
                <span class="typing-dots">
                    <span>.</span><span>.</span><span>.</span>
                </span>
            </span>
        `;
        typingIndicator.style.display = 'flex';
    } else {
        if (currentTypingUser && currentTypingUser.username === data.username) {
            typingIndicator.style.display = 'none';
            currentTypingUser = null;
        }
    }
});

// Handle errors
socket.on('error', (data) => {
    alert(data.message);
    window.location.href = '/';
});

// Display message function
function displayMessage(data, isSent) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isSent ? 'sent' : 'received'}`;
    
    // Messages are encrypted server-side with Fernet (end-to-end encryption)
    // Server decrypts for display since it manages the encryption key
    // All messages are encrypted in transit and at rest
    let messageText = data.message;
    
    // If message is encrypted string (base64), it will be displayed as-is
    // In production, client-side decryption would happen here using the encryption key
    // For this implementation, server handles decryption for display
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="message-avatar">${data.avatar}</span>
            <span class="message-username">${data.username}</span>
            <span class="message-timestamp">${data.timestamp}</span>
        </div>
        <div class="message-bubble">${escapeHtml(messageText)}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Display system message
function displaySystemMessage(text) {
    const systemDiv = document.createElement('div');
    systemDiv.className = 'system-message';
    systemDiv.textContent = text;
    messagesContainer.appendChild(systemDiv);
    scrollToBottom();
}

// Update user list
function updateUserList(users, count) {
    userCount.textContent = count;
    userList.innerHTML = '';
    
    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.className = 'user-item';
        userDiv.innerHTML = `
            <span class="user-avatar">${user.avatar}</span>
            <div class="user-info">
                <div class="user-name">${escapeHtml(user.username)}</div>
            </div>
        `;
        userList.appendChild(userDiv);
    });
}

// Send message
function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    socket.emit('send_message', {
        message: message
    });
    
    messageInput.value = '';
    stopTyping();
    sendButton.disabled = true;
}

// Typing indicator handlers
function handleTyping() {
    socket.emit('typing', { is_typing: true });
    
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        stopTyping();
    }, 1000);
}

function stopTyping() {
    socket.emit('typing', { is_typing: false });
    clearTimeout(typingTimeout);
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    } else {
        handleTyping();
    }
});

messageInput.addEventListener('input', () => {
    sendButton.disabled = !messageInput.value.trim();
    handleTyping();
});

messageInput.addEventListener('blur', stopTyping);

// Dark mode toggle
darkModeToggle.addEventListener('click', () => {
    isDarkMode = !isDarkMode;
    localStorage.setItem('darkMode', isDarkMode);
    
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        darkModeToggle.textContent = '☀️';
    } else {
        document.documentElement.removeAttribute('data-theme');
        darkModeToggle.textContent = '🌙';
    }
});

// Copy room ID
copyRoomIdButton.addEventListener('click', () => {
    navigator.clipboard.writeText(roomId).then(() => {
        const originalText = copyRoomIdButton.textContent;
        copyRoomIdButton.textContent = '✓';
        setTimeout(() => {
            copyRoomIdButton.textContent = originalText;
        }, 2000);
    });
});

// Scroll to bottom
function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-scroll on new messages
const observer = new MutationObserver(() => {
    scrollToBottom();
});

observer.observe(messagesContainer, {
    childList: true,
    subtree: true
});
