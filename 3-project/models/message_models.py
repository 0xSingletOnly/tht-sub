from dataclasses import dataclass

@dataclass
class WhatsAppMessage:
    phone_number: str
    message_text: str
    template_name: str = None
