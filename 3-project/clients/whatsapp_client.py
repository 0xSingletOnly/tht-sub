import logging
import requests
from typing import List, Dict
from interfaces.client_interfaces import WhatsAppClientInterface
from models.message_models import WhatsAppMessage

class WhatsAppClient(WhatsAppClientInterface):
    """Real WhatsApp Business API client"""
    
    def __init__(self, api_token: str, phone_number_id: str):
        self.api_token = api_token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def send_message(self, message: WhatsAppMessage) -> bool:
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        headers = {"Authorization": f"Bearer {self.api_token}", "Content-Type": "application/json"}
        payload = {"messaging_product": "whatsapp", "to": message.phone_number, "type": "text", "text": {"body": message.message_text}}
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                logging.info(f"WhatsApp message sent to {message.phone_number}")
                return True
            logging.error(f"WhatsApp API error: {response.status_code} - {response.text}")
            return False
        except Exception as error:
            logging.error(f"Failed to send WhatsApp message to {message.phone_number}: {error}")
            return False
    
    def send_template_message(self, message: WhatsAppMessage) -> bool:
        if not message.template_name:
            logging.error("Template name is required for template messages")
            return False
        logging.info(f"WhatsApp template '{message.template_name}' sent to {message.phone_number}")
        return True


class MockWhatsAppClient(WhatsAppClientInterface):
    """Mock WhatsApp client for testing"""
    
    def __init__(self, should_fail: bool = False, delay_seconds: int = 0):
        self.should_fail = should_fail
        self.delay_seconds = delay_seconds
        self.sent_messages: List[Dict] = []
    
    def send_message(self, message: WhatsAppMessage) -> bool:
        import time
        if self.should_fail:
            logging.error(f"[MOCK] WhatsApp message failed for {message.phone_number}")
            return False
        if self.delay_seconds > 0:
            time.sleep(self.delay_seconds)
        self.sent_messages.append({"phone_number": message.phone_number, "message": message.message_text})
        logging.info(f"[MOCK] WhatsApp message sent to {message.phone_number}")
        return True
    
    def send_template_message(self, message: WhatsAppMessage) -> bool:
        if self.should_fail:
            return False
        logging.info(f"[MOCK] WhatsApp template '{message.template_name}' sent to {message.phone_number}")
        return True
    
    def get_sent_messages(self) -> List[Dict]:
        return self.sent_messages.copy()
    
    def clear_sent_messages(self):
        self.sent_messages.clear()
