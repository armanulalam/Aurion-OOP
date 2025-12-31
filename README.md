# 🤖 Aurion - Personal AI Assistant

A sophisticated Personal AI Assistant built with **Gemini API**, **Object-Oriented Programming (OOP)**, **Streamlit**, and **MongoDB**. Aurion provides intelligent assistance for learning, coding, productivity, and general queries with a modern ChatGPT-like interface.

## 🎥 Demo Video

https://youtu.be/KabooJ-ubr0

---

## ✨ Features

### Core Capabilities
- 💬 **ChatGPT-like Interface** - Clean, modern chat interface
- 🔐 **User Authentication** - Secure login and signup with MongoDB
- 🧠 **Context Memory** - Maintains conversation history across sessions
- 💾 **Persistent Storage** - Conversations saved permanently in MongoDB
- 🎭 **Multiple Modes** - General Assistant, Tutor, Coder, Career Mentor
- 💬 **Multi-Conversation Support** - Create and manage multiple conversations
- ⚡ **Streaming Responses** - Real-time response generation
- 🎤 **Voice Commands** - Speak to Aurion and get text responses
- 📱 **Cross-Device Access** - Access your conversations from anywhere

### OOP Architecture
- ✅ **Classes & Objects** - Well-structured class hierarchy
- ✅ **Encapsulation** - Data hiding and controlled access
- ✅ **Inheritance** - Reusable and extensible code
- ✅ **Modular Design** - Separation of concerns

### Security Features
- 🔐 **Password Hashing** - SHA-256 encryption for secure password storage
- 🔐 **Secure Sessions** - Server-side session management with Streamlit
- 🔐 **User Data Isolation** - Each user's conversations are private
- 🔐 **Environment Variables** - API keys and sensitive data protection

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Streamlit** - Web interface
- **Google Gemini API** - AI intelligence
- **MongoDB** - Database for user authentication and data persistence
- **PyMongo** - MongoDB driver for Python
- **SpeechRecognition** - Voice input processing
- **python-dotenv** - Environment management

---

## 📁 Project Structure
```
Aurion-OOp/
│
├── app.py                      # Main Streamlit application
│
├── auth/                       # Authentication system
│   ├── __init__.py
│   └── auth_ui.py             # Login/Signup UI components
│
├── database/                   # Database management
│   ├── __init__.py
│   └── db_handler.py          # MongoDB operations & user management
│
├── aurion/                     # Core Aurion modules
│   ├── __init__.py
│   ├── assistant.py            # Main assistant orchestrator
│   ├── gemini_engine.py        # Gemini API handler
│   ├── prompt_controller.py    # System prompts & personality
│   ├── memory.py               # Temporary conversation storage
│   ├── user_memory.py          # Persistent user conversations (MongoDB)
│   └── voice_handler.py        # Voice recognition handler
│
├── config/                     # Configuration management
│   ├── __init__.py
│   └── settings.py             # Environment & settings
│
├── data/                       # Data storage (auto-created)
│   └── memory.json            # Conversation backup
│
├── .env                        # API keys & MongoDB URI (create this)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/armanulalam/Aurion-OOP.git
cd Aurion-OOP
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
conda create -n oopaurion python=3.9 -y
conda activate oopaurion
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MongoDB

Choose one option:

#### **Option A: MongoDB Atlas (Cloud - Recommended)**

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account and M0 cluster (free tier)
3. Create a database user with username and password
4. Whitelist your IP address (or use 0.0.0.0/0 for development)
5. Get your connection string from "Connect" → "Connect your application"

Example connection string:
```
mongodb+srv://username:password@cluster.mongodb.net/aurion?retryWrites=true&w=majority
```

#### **Option B: Local MongoDB**

**Windows:**
1. Download from https://www.mongodb.com/try/download/community
2. Install MongoDB Community Server
3. MongoDB runs on `mongodb://localhost:27017/`

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### 5. Set Up Environment Variables

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```env
# Gemini API Key (Required)
GEMINI_API_KEY=your_actual_api_key_here

# MongoDB Connection String (Required)
# For Local MongoDB:
MONGODB_URI=mongodb://localhost:27017/

# For MongoDB Atlas (Cloud):
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/aurion?retryWrites=true&w=majority
```

**Get Gemini API Key:** https://makersuite.google.com/app/apikey

### 6. Verify Installation

Run the dependency checker:
```bash
python check_dependencies.py
```

This will verify:
- ✅ Python version
- ✅ All packages installed correctly
- ✅ MongoDB connection working
- ✅ Gemini API key configured

### 7. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### 🔐 First Time Setup

1. **Create Account**
   - Open the app
   - Click "📝 Create New Account"
   - Enter your name, email, and password (minimum 6 characters)
   - Click "✅ Sign Up"

2. **Login**
   - Enter your registered email and password
   - Click "🔐 Login"
   - Your previous conversations will be automatically loaded

### Starting a Conversation

1. **Application starts** - A default conversation is created automatically
2. **Select Mode** - Choose your preferred assistant mode from sidebar
3. **Start Chatting** - Type your message in the input box or use voice input

### Managing Conversations

- **New Conversation** - Click "➕ New Conversation" in sidebar
- **Switch Conversations** - Click on any conversation in the list
- **Delete Conversation** - Click the 🗑️ button next to a conversation
- **Clear Conversation** - Use "🧹 Clear Conversation" to reset current chat
- **All conversations persist** - Logout and login anytime, your chats are saved!

### Voice Commands 🎤

1. Click the **🎤** button next to the chat input
2. Wait for "Listening..." prompt
3. Speak your question clearly
4. Your speech will be converted to text
5. Aurion will respond automatically

### Assistant Modes

#### 🤖 General Assistant
- **Best for:** Everyday questions, general help
- **Example:** "What is blockchain technology?"

#### 📚 Learning Tutor
- **Best for:** Study help, concept explanations
- **Example:** "Explain calculus derivatives step by step"

#### 💻 Coding Assistant
- **Best for:** Programming help, debugging
- **Example:** "Write a Python function to sort a list"

#### 🎯 Career Mentor
- **Best for:** Career advice, professional development
- **Example:** "How do I prepare for a data science interview?"

---

## 🗄️ Database Architecture

### MongoDB Collections

#### **users** Collection
Stores user account information:
```javascript
{
  "_id": ObjectId("..."),
  "name": "John Doe",
  "email": "john@example.com",
  "password": "hashed_sha256_password",  // SHA-256 hashed
  "created_at": ISODate("2025-12-26T10:00:00Z"),
  "last_login": ISODate("2025-12-26T15:30:00Z")
}
```

#### **user_conversations** Collection
Stores all conversations for each user:
```javascript
{
  "_id": ObjectId("..."),
  "user_id": "user_object_id",  // Links to users collection
  "conversations": {
    "conv_abc123": [
      {
        "role": "user",
        "message": "Hello Aurion",
        "timestamp": "2025-12-26T10:00:00"
      },
      {
        "role": "assistant",
        "message": "Hello! How can I help you?",
        "timestamp": "2025-12-26T10:00:05"
      }
    ],
    "conv_xyz456": [ /* more messages */ ]
  },
  "updated_at": ISODate("2025-12-26T15:30:00Z")
}
```

### Data Persistence Flow

```
User Login
    ↓
UserMemory loads conversations from MongoDB
    ↓
User sees all previous conversations
    ↓
User sends message
    ↓
Message instantly saved to MongoDB
    ↓
User logs out
    ↓
All data remains in MongoDB
    ↓
User logs in again
    ↓
All conversations restored! ✨
```

### Database Connection

The `DatabaseHandler` class manages all MongoDB operations:

**Key Methods:**
- `register_user()` - Create new user account
- `login_user()` - Authenticate user credentials
- `save_user_conversations()` - Save conversations to database
- `load_user_conversations()` - Load user's conversation history
- `is_connected()` - Check database connection status

**Example Usage:**
```python
from database import DatabaseHandler

# Initialize connection
db = DatabaseHandler()

# Register new user
result = db.register_user("John Doe", "john@example.com", "password123")

# Login user
result = db.login_user("john@example.com", "password123")

# Save conversations
db.save_user_conversations(user_id, conversations)
```

---

## 🏗 OOP Architecture

### Class Hierarchy
```
Settings
   ↓
DatabaseHandler (MongoDB) ←──┐
   ↓                         │
GeminiEngine ←──┐             │
                │             │
PromptController ←─┼→ Assistant → Streamlit App
                │             │
UserMemory ←────┴─────────────┘
   ↓
VoiceHandler
```

### Key Classes

#### 1. **DatabaseHandler** (`database/db_handler.py`)
- Manages MongoDB connection and operations
- Handles user authentication (registration, login)
- Stores and retrieves user conversations
- Password hashing with SHA-256

#### 2. **GeminiEngine** (`aurion/gemini_engine.py`)
- Manages Gemini API connection
- Handles response generation
- Supports streaming responses

#### 3. **PromptController** (`aurion/prompt_controller.py`)
- Defines assistant personalities (4 modes)
- Manages system prompts
- Builds contextualized prompts

#### 4. **Memory** (`aurion/memory.py`)
- Temporary conversation storage (file-based)
- Used for non-authenticated users
- Manages multiple conversations

#### 5. **UserMemory** (`aurion/user_memory.py`)
- Persistent conversation storage (database-backed)
- Automatically loads conversations on login
- Saves every message to MongoDB
- Used for authenticated users

#### 6. **Assistant** (`aurion/assistant.py`)
- Main orchestrator
- Coordinates all components
- Manages conversation flow

#### 7. **Settings** (`config/settings.py`)
- Environment configuration
- API key and MongoDB URI management
- Path handling

#### 8. **VoiceHandler** (`aurion/voice_handler.py`)
- Speech recognition
- Microphone input handling
- Voice-to-text conversion

#### 9. **Auth UI Functions** (`auth/auth_ui.py`)
- Login and signup pages
- User profile display in sidebar
- Session management

---

## 🔐 Security Features

### Password Security
- **SHA-256 Hashing** - All passwords are hashed before storage
- **No Plain Text** - Passwords never stored in readable format
- **Salted Hashing** - Enhanced security through password hashing

### Session Security
- **Server-Side Sessions** - Streamlit manages sessions securely
- **Auto Logout** - Session clears on logout
- **No Token Exposure** - Session-based authentication

### Database Security
- **Connection String Protection** - Stored in .env file (not in code)
- **User Isolation** - Each user can only access their own data
- **Input Validation** - All inputs validated before database operations

### Best Practices
- ✅ Always use `.env` for sensitive data
- ✅ Never commit `.env` to Git (included in `.gitignore`)
- ✅ Use MongoDB Atlas with IP whitelisting for production
- ✅ Enable MongoDB authentication in production
- ✅ Use strong passwords (8+ characters, mixed case, numbers)

---

## 🧪 Testing

### Test Database Connection

```bash
# Run diagnostic script
python check_dependencies.py

# Or test manually
python -c "from database import DatabaseHandler; db = DatabaseHandler(); print('✅ Connected!' if db.is_connected() else '❌ Failed')"
```

### Test User Registration & Login

```python
from database import DatabaseHandler

db = DatabaseHandler()

# Test registration
result = db.register_user("Test User", "test@example.com", "test123")
print(result)  # Should show success

# Test login
result = db.login_user("test@example.com", "test123")
print(result)  # Should return user data
```

### Verify in MongoDB

```bash
# Open MongoDB shell
mongosh

# Switch to database
use aurion

# View users
db.users.find().pretty()

# View conversations
db.user_conversations.find().pretty()
```

---

## 🐛 Troubleshooting

### MongoDB Connection Issues

**Problem:** "Failed to connect to MongoDB"

**Solutions:**
```bash
# Check if MongoDB is running (local)
sudo systemctl status mongodb  # Linux
brew services list | grep mongodb  # Mac

# Start MongoDB
sudo systemctl start mongodb  # Linux
brew services start mongodb-community  # Mac

# Test connection
mongosh mongodb://localhost:27017/

# For Atlas: Check IP whitelist in MongoDB Atlas dashboard
```

### Import Errors

**Problem:** `Import "pymongo" could not be resolved`

**Solutions:**
```bash
# Install pymongo
pip install pymongo

# If using virtual environment, make sure it's activated
# VS Code: Select correct Python interpreter (Ctrl+Shift+P)

# See detailed guide
# Read: FIXING_IMPORTS.md
```

### Voice Commands Not Working

**Problem:** Microphone not detected or speech not recognized

**Solutions:**
```bash
# Install audio dependencies
# Windows: See VOICE_SETUP.md for PyAudio installation
# Mac: brew install portaudio
# Linux: sudo apt-get install portaudio19-dev python3-pyaudio

# Grant microphone permissions in browser/system settings

# Test microphone
python -c "from aurion import VoiceHandler; print(VoiceHandler().is_microphone_available())"
```

### Password/Login Issues

**Problem:** "Invalid email or password"

**Solutions:**
- Verify email is correct (case-insensitive)
- Password is case-sensitive
- Ensure you registered first
- Try resetting: Delete user from MongoDB and re-register

---

## 💾 Persistent Conversations

**Your conversations are now permanent!**

### How It Works

1. **On Login** - All your previous conversations are loaded from MongoDB
2. **While Chatting** - Every message is automatically saved to the database
3. **On Logout** - Your conversations remain safely stored in MongoDB
4. **Next Login** - Everything is restored exactly as you left it

### Benefits

- ✅ **Never Lose Data** - Conversations persist forever
- ✅ **Cross-Device** - Access from any device by logging in
- ✅ **Multiple Users** - Each user has their own private conversations
- ✅ **Automatic Saving** - No manual save needed
- ✅ **History Preserved** - Full conversation context maintained

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Object-Oriented Programming principles
- ✅ API integration and error handling
- ✅ Database design and operations (MongoDB)
- ✅ User authentication and session management
- ✅ State management in web applications
- ✅ File I/O and data persistence
- ✅ User interface design with Streamlit
- ✅ Clean code architecture and modularity
- ✅ Security best practices (password hashing, environment variables)
- ✅ Speech recognition integration

---

## 📚 Additional Documentation

- **QUICKSTART.md** - Quick setup guide
- **MONGODB_SETUP.md** - Detailed MongoDB installation and configuration
- **VOICE_SETUP.md** - Voice commands setup and troubleshooting
- **AUTH_COMPLETE.md** - Authentication system implementation guide
- **PERSISTENT_CONVERSATIONS.md** - Conversation persistence details
- **FIXING_IMPORTS.md** - Import error troubleshooting

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **Google Gemini** - For the powerful AI API
- **MongoDB** - For the database platform
- **Streamlit** - For the amazing web framework
- **Python Community** - For excellent libraries

---

## 📞 Support

For questions or issues:
- **Email:** armaanularmaan@gmail.com
- **GitHub Issues:** [Create an issue](https://github.com/armanulalam/Aurion-OOP/issues)
