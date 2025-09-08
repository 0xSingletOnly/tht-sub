from typing import Dict
from clients.whatsapp_client import WhatsAppClient, MockWhatsAppClient
from clients.email_client import EmailClient, MockEmailClient
from interfaces.client_interfaces import WhatsAppClientInterface, EmailClientInterface

def create_whatsapp_client(use_mock: bool = False, mock_config: Dict = None) -> WhatsAppClientInterface:
    if use_mock:
        config = mock_config or {}
        return MockWhatsAppClient(
            should_fail=config.get('should_fail', False),
            delay_seconds=config.get('delay_seconds', 0)
        )
    return WhatsAppClient(api_token="your_whatsapp_api_token", phone_number_id="your_phone_number_id")


def create_email_client(use_mock: bool = False, mock_config: Dict = None) -> EmailClientInterface:
    if use_mock:
        config = mock_config or {}
        return MockEmailClient(should_fail=config.get('should_fail', False))
    return EmailClient(smtp_config={"host": "smtp.example.com", "port": 587})
