from abc import ABC, abstractmethod
from models.message_models import WhatsAppMessage

class WhatsAppClientInterface(ABC):
    @abstractmethod
    def send_message(self, message: WhatsAppMessage) -> bool:
        pass
    
    @abstractmethod
    def send_template_message(self, message: WhatsAppMessage) -> bool:
        pass


class EmailClientInterface(ABC):
    @abstractmethod
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        pass
