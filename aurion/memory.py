import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class Memory:
    """
    Manages conversation memory using a single JSON file
    """
    
    def __init__(self, memory_file: str = "data/memory.json"):
        self.memory_file = memory_file
        self.conversations: Dict[str, List[Dict]] = {}
        self.current_conversation_id: Optional[str] = None
        self._load_memory()
        
    def _load_memory(self) -> None:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversations = data.get('conversations', {})
                    self.current_conversation_id = data.get('current_conversation_id')
            except Exception as e:
                print(f"Error loading memory: {e}")
                self.conversations = {}
        else:
            self.conversations = {}
            
    def _save_memory(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            
            data = {
                'conversations': self.conversations,
                'current_conversation_id': self.current_conversation_id,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def create_conversation(self, conversation_id: str) -> None:
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        self.current_conversation_id = conversation_id
        self._save_memory()
    
    def set_current_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self.conversations:
            self.current_conversation_id = conversation_id
            self._save_memory()
            return True
        return False
    
    def add(self, role: str, message: str, conversation_id: Optional[str] = None) -> None:
        conv_id = conversation_id or self.current_conversation_id
        
        if conv_id is None:
            conv_id = "default"
            self.create_conversation(conv_id)
        
        if conv_id not in self.conversations:
            self.conversations[conv_id] = []
        
        self.conversations[conv_id].append({
            'role': role,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        self._save_memory()
        
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
            self._save_memory()
    
    def delete_conversation(self, conversation_id: str) -> None:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            
            if self.current_conversation_id == conversation_id:
                self.current_conversation_id = None
                
            self._save_memory()
    
    def get_all_conversations(self) -> Dict[str, List[Dict]]:
        return self.conversations
    
    def get_conversation_ids(self) -> List[str]:
        return list(self.conversations.keys())
    
    def get_message_count(self, conversation_id: Optional[str] = None) -> int:
        conv_id = conversation_id or self.current_conversation_id
        
        if conv_id and conv_id in self.conversations:
            return len(self.conversations[conv_id])
        return 0    