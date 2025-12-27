import speech_recognition as sr
from typing import Optional

class VoiceHandler:
    """
    Handles voice input using speech recognition
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def recognize_speech_from_mic(self, timeout: int = 5, phrase_time_limit: int = 30) -> Optional[str]:
        try:
            with sr.Microphone() as source:
                print("I am Listening... Speak now!")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
                print("Processing speech...")
                
                text = self.recognizer.recognize_google(audio)
                return text
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service; {e}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def is_microphone_available(self) -> bool:
        try:
            with sr.Microphone() as source:
                return True
        except Exception:
            return False