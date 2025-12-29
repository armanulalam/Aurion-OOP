"""
User Memory Module - Database-backed conversation storage per user
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class UserMemory:
    """
    Manages conversation memory for a specific user with database persistence
    """
    
    def __init__(self, user_id: str, db_handler=None):
        self.user_id = user_id
        self.db_handler = db_handler
        self.conversations: Dict[str, List[Dict]] = {}
        self.current_conversation_id: Optional[str] = None
        self._load_from_database()
        
    def _load_from_database(self) -> None:
        if self.db_handler:
            try:
                self.conversations = self.db_handler.load_user_conversations(self.user_id)
                print(f"✅ Loaded {len(self.conversations)} conversations for user {self.user_id}")
            except Exception as e:
                print(f"Error loading from database: {e}")
                self.conversations = {}
        else:
            self.conversations = {}
            
    def _save_to_database(self) -> None:
        if self.db_handler:
            try:
                self.db_handler.save_user_conversations(self.user_id, self.conversations)
            except Exception as e:
                print(f"Error saving to database: {e}")
    
    def create_conversation(self, conversation_id: str) -> None:
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        self.current_conversation_id = conversation_id
        self._save_to_database()
    
    def set_current_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self.conversations:
            self.current_conversation_id = conversation_id
            return True
        return False
    
    def add(self, role: str, message: str, conversation_id: Optional[str] = None) -> None:
        conv_id = conversation_id or self.current_conversation_id
        
        if conv_id is None:
            # Create a default conversation if none exists
            conv_id = "default"
            self.create_conversation(conv_id)
        
        if conv_id not in self.conversations:
            self.conversations[conv_id] = []
        
        self.conversations[conv_id].append({
            'role': role,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        self._save_to_database()
        
    def get_history(self, conversation_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, str]]:
        conv_id = conversation_id or self.current_conversation_id
        
        if conv_id is None or conv_id not in self.conversations:
            return []
        
        history = self.conversations[conv_id]
        
        if limit:
            return history[-limit:]
        return history
    
    def get_formatted_history(self, conversation_id: Optional[str] = None, limit: Optional[int] = None) -> str:
        history = self.get_history(conversation_id, limit)
        formatted = []
        
        for msg in history:
            role = "User" if msg['role'] == 'user' else "Assistant"
            formatted.append(f"{role}: {msg['message']}")
            
        return "\n".join(formatted)
    
    def clear(self, conversation_id: Optional[str] = None) -> None:
        conv_id = conversation_id or self.current_conversation_id
        
        if conv_id and conv_id in self.conversations:
            self.conversations[conv_id] = []
            self._save_to_database()
    
    def delete_conversation(self, conversation_id: str) -> None:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            
            # If deleting current conversation, clear current_conversation_id
            if self.current_conversation_id == conversation_id:
                self.current_conversation_id = None
                
            self._save_to_database()
    
    def get_all_conversations(self) -> Dict[str, List[Dict]]:
        return self.conversations
    
    def get_conversation_ids(self) -> List[str]:
        return list(self.conversations.keys())
    
    def get_message_count(self, conversation_id: Optional[str] = None) -> int:
        conv_id = conversation_id or self.current_conversation_id
        
        if conv_id and conv_id in self.conversations:
            return len(self.conversations[conv_id])
        return 0
    
    def clear_all_conversations(self) -> None:
        self.conversations = {}
        self.current_conversation_id = None
        self._save_to_database()