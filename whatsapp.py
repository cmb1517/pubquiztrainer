import requests
import os

from decorators import retry
from logger import setup_logger

logger = setup_logger("whatsapp")

# Docker-aware configuration
# WAHA_URL = os.getenv("WAHA_URL", "http://localhost:3000/api/sendText")
# # Pull from .env file via Docker environment
# API_KEY = os.getenv("WAHA_API_KEY", "your_fallback_local_key")
# GROUP_ID = os.getenv("WHATSAPP_GROUP_ID", "your_fallback_local_group")
BASE_URL = os.getenv("WAHA_URL", "http://waha:3000").split("/api")[0].rstrip("/")
API_KEY = os.getenv("WAHA_API_KEY")
GROUP_ID = os.getenv("WHATSAPP_GROUP_ID")

def ensure_session_working():
    headers = {"X-Api-Key": API_KEY}
    try:
        response = requests.get(f"{BASE_URL}/api/sessions", headers=headers)
        response.raise_for_status()
        sessions = response.json()
        
        default_session = next((s for s in sessions if s.get('name') == 'default'), None)
        
        if not default_session or default_session.get('status') != 'WORKING':
            status = default_session.get('status') if default_session else "MISSING"
            logger.warning(f"Session 'default' is {status}. Sending start command...")
            requests.post(f"{BASE_URL}/api/sessions/start", json={"name": "default"}, headers=headers)
            return False
            
        return True
    except Exception as e:
        logger.error(f"Failed to check/start session: {e}")
        return False

@retry(max_tries=5, initial_delay=1, backoff_factor=2)
def send_message(text):
    if not ensure_session_working():
        raise Exception("WhatsApp session was STOPPED. Kickstarted it, but need to retry...")
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json",
    }
    
    payload = {
        "chatId": GROUP_ID,
        "text": text,
        "session": "default"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/sendText", json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"✅ Message sent to {GROUP_ID}")
    except Exception as e:
        logger.error(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Server said: {e.response.text}")
        raise e

if __name__ == "__main__":
    send_message("The Pub Quiz engine is officially online! 🍻")

    