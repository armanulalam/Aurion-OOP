# 🤖 Aurion - Personal AI Assistant

A sophisticated Personal AI Assistant built with **Gemini API**, **Object-Oriented Programming (OOP)**, and **Streamlit**. Aurion provides intelligent assistance for learning, coding, productivity, and general queries with a modern ChatGPT-like interface.

## 🎥 Demo Video

**[Insert Your Demo Video Link Here]**

---

## ✨ Features

### Core Capabilities
- 💬 **ChatGPT-like Interface** - Clean, modern chat interface
- 🧠 **Context Memory** - Maintains conversation history across sessions
- 🎭 **Multiple Modes** - General Assistant, Tutor, Coder, Career Mentor
- 💬 **Multi-Conversation Support** - Create and manage multiple conversations
- ⚡ **Streaming Responses** - Real-time response generation
- 💾 **Persistent Storage** - All conversations saved in JSON format

### OOP Architecture
- ✅ **Classes & Objects** - Well-structured class hierarchy
- ✅ **Encapsulation** - Data hiding and controlled access
- ✅ **Inheritance** - Reusable and extensible code
- ✅ **Modular Design** - Separation of concerns

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Streamlit** - Web interface
- **Google Gemini API** - AI intelligence
- **python-dotenv** - Environment management

---

## 📁 Project Structure
```
Aurion-OOp/
│
├── app.py                      # Main Streamlit application
│
├── aurion/                     # Core Aurion modules
│   ├── __init__.py
│   ├── assistant.py            # Main assistant orchestrator
│   ├── gemini_engine.py        # Gemini API handler
│   ├── prompt_controller.py    # System prompts & personality
│   └── memory.py               # Conversation memory management
|   ├── voice_handler.py        # handles voice input
│
├── config/                     # Configuration management
│   ├── __init__.py
│   └── settings.py             # Environment & settings
│
├── data/                       # Data storage (auto-created)
│   └── memory.json            # Conversation history
│
├── .env                        # API keys (create this)
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
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Starting a Conversation

1. **Application starts** - A default conversation is created automatically
2. **Select Mode** - Choose your preferred assistant mode from sidebar
3. **Start Chatting** - Type your message in the input box

### Managing Conversations

- **New Conversation** - Click "➕ New Conversation" in sidebar
- **Switch Conversations** - Click on any conversation in the list
- **Delete Conversation** - Click the 🗑️ button next to a conversation
- **Clear Conversation** - Use "🧹 Clear Conversation" to reset current chat

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

## 🏗 OOP Architecture

### Class Hierarchy
```
Settings
   ↓
GeminiEngine ←──┐
                │
PromptController ←─┼→ Assistant → Streamlit App
                │
Memory ←────────┘
```

### Key Classes

#### 1. **GeminiEngine** (`aurion/gemini_engine.py`)
- Manages Gemini API connection
- Handles response generation
- Supports streaming responses

#### 2. **PromptController** (`aurion/prompt_controller.py`)
- Defines assistant personalities
- Manages system prompts
- Builds contextualized prompts

#### 3. **Memory** (`aurion/memory.py`)
- Stores conversation history in single JSON file
- Manages multiple conversations
- Provides context retrieval

#### 4. **Assistant** (`aurion/assistant.py`)
- Main orchestrator
- Coordinates all components
- Manages conversation flow

#### 5. **Settings** (`config/settings.py`)
- Environment configuration
- API key management
- Path handling

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Object-Oriented Programming principles
- ✅ API integration and error handling
- ✅ State management in web applications
- ✅ File I/O and data persistence
- ✅ User interface design with Streamlit
- ✅ Clean code architecture and modularity

---