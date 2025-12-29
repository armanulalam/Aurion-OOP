from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import hashlib
import os
from typing import Optional, Dict
from datetime import datetime


class DatabaseHandler:
    """
    Handles MongoDB connection and user authentication
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or os.getenv("MONGODB_URI")
        self.client = None
        self.db = None
        self.users_collection = None
        self._connect()
        
    def _connect(self) -> bool:
        try:
            self.client = MongoClient(self.connection_string)
            # Test connection
            self.client.admin.command('ping')
            
            # Get database and collections
            self.db = self.client['UserDetails']
            self.users_collection = self.db['users']
            
            # Create unique index on email
            self.users_collection.create_index("email", unique=True)
            
            print("✅ Connected to MongoDB successfully")
            return True
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, name: str, email: str, password: str) -> Dict[str, any]:
        
        try:
            # Validate inputs
            if not name or not email or not password:
                return {'success': False, 'message': 'All fields are required'}
            
            if len(password) < 6:
                return {'success': False, 'message': 'Password must be at least 6 characters'}
            
            # Check if email already exists
            if self.users_collection.find_one({'email': email}):
                return {'success': False, 'message': 'Email already registered'}
            
            # Create user document
            user_doc = {
                'name': name,
                'email': email.lower(),
                'password': self._hash_password(password),
                'created_at': datetime.now(),
                'last_login': None
            }
            
            # Insert user
            result = self.users_collection.insert_one(user_doc)
            
            return {
                'success': True,
                'message': 'Registration successful',
                'user_id': str(result.inserted_id)
            }
            
        except DuplicateKeyError:
            return {'success': False, 'message': 'Email already registered'}
        except Exception as e:
            return {'success': False, 'message': f'Registration failed: {str(e)}'}
    
    def login_user(self, email: str, password: str) -> Dict[str, any]:
        try:
            # Validate inputs
            if not email or not password:
                return {'success': False, 'message': 'Email and password required'}
            
            # Find user
            user = self.users_collection.find_one({'email': email.lower()})
            
            if not user:
                return {'success': False, 'message': 'Invalid email or password'}
            
            # Verify password
            if user['password'] != self._hash_password(password):
                return {'success': False, 'message': 'Invalid email or password'}
            
            # Update last login
            self.users_collection.update_one(
                {'_id': user['_id']},
                {'$set': {'last_login': datetime.now()}}
            )
            
            # Return user data (without password)
            user_data = {
                'user_id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'created_at': user['created_at']
            }
            
            return {
                'success': True,
                'message': 'Login successful',
                'user': user_data
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Login failed: {str(e)}'}
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        try:
            from bson import ObjectId
            user = self.users_collection.find_one({'_id': ObjectId(user_id)})
            
            if user:
                return {
                    'user_id': str(user['_id']),
                    'name': user['name'],
                    'email': user['email'],
                    'created_at': user['created_at']
                }
            return None
            
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_user_profile(self, user_id: str, name: Optional[str] = None, 
                           password: Optional[str] = None) -> Dict[str, any]:
        try:
            from bson import ObjectId
            update_fields = {}
            
            if name:
                update_fields['name'] = name
            
            if password:
                if len(password) < 6:
                    return {'success': False, 'message': 'Password must be at least 6 characters'}
                update_fields['password'] = self._hash_password(password)
            
            if not update_fields:
                return {'success': False, 'message': 'No fields to update'}
            
            result = self.users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_fields}
            )
            
            if result.modified_count > 0:
                return {'success': True, 'message': 'Profile updated successfully'}
            else:
                return {'success': False, 'message': 'No changes made'}
                
        except Exception as e:
            return {'success': False, 'message': f'Update failed: {str(e)}'}
    
    def is_connected(self) -> bool:
        try:
            if self.client:
                self.client.admin.command('ping')
                return True
            return False
        except:
            return False
    
    def close_connection(self):
        if self.client:
            self.client.close()
            print("Database connection closed")
    
    def save_user_conversations(self, user_id: str, conversations: Dict) -> bool:
        try:
            from bson import ObjectId
            
            # Update or create user's conversations document
            result = self.db['user_conversations'].update_one(
                {'user_id': user_id},
                {
                    '$set': {
                        'user_id': user_id,
                        'conversations': conversations,
                        'updated_at': datetime.now()
                    }
                },
                upsert=True
            )
            
            return True
            
        except Exception as e:
            print(f"Error saving conversations: {e}")
            return False
    
    def load_user_conversations(self, user_id: str) -> Dict:
        try:
            # Get user's conversations document
            user_convs = self.db['user_conversations'].find_one({'user_id': user_id})
            
            if user_convs and 'conversations' in user_convs:
                return user_convs['conversations']
            
            return {}
            
        except Exception as e:
            print(f"Error loading conversations: {e}")
            return {}
    
    def delete_user_conversations(self, user_id: str) -> bool:
        try:
            self.db['user_conversations'].delete_one({'user_id': user_id})
            return True
        except Exception as e:
            print(f"Error deleting conversations: {e}")
            return False