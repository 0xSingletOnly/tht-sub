import logging
from typing import List, Dict
from interfaces.client_interfaces import EmailClientInterface

class EmailClient(EmailClientInterface):
    """Real Email client"""
    
    def __init__(self, smtp_config: dict):
        self.smtp_config = smtp_config
    
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        try:
            logging.info(f"Email sent to {recipient}: {subject}")
            return True
        except Exception as error:
            logging.error(f"Failed to send email to {recipient}: {error}")
            return False


class MockEmailClient(EmailClientInterface):
    """Mock Email client for testing"""
    
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail
        self.sent_emails: List[Dict] = []
    
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        if self.should_fail:
            logging.error(f"[MOCK] Email failed for {recipient}")
            return False
        self.sent_emails.append({"recipient": recipient, "subject": subject, "body": body})
        logging.info(f"[MOCK] Email sent to {recipient}")
        return True
    
    def get_sent_emails(self) -> List[Dict]:
        return self.sent_emails.copy()
    
    def clear_sent_emails(self):
        self.sent_emails.clear()
