import logging
from typing import List, Dict, Any
from psycopg2.extras import DictCursor

from clients.whatsapp_client import WhatsAppMessage
from interfaces.client_interfaces import WhatsAppClientInterface, EmailClientInterface

# Mapping confident predicted intents to next steps
INTENT_TO_ACTION_MAP = {
    "voice_wants_email_follow_up": "send_email",
    "voice_wants_whatsapp_sms_follow_up": "send_whatsapp", 
    "voice_wrong_number": "send_email", # contact via non-phone methods
}

def should_process_intent(intent: str) -> bool:
    return intent in INTENT_TO_ACTION_MAP

def get_next_action_for_intent(intent: str) -> str:
    return INTENT_TO_ACTION_MAP.get(intent, "human_review")


class VoiceCallProcessor:
    def __init__(
        self,
        db_connection,
        whatsapp_client: WhatsAppClientInterface = None,
        email_client: EmailClientInterface = None,
    ):
        self.connection = db_connection
        self.whatsapp_client = whatsapp_client
        self.email_client = email_client

    def get_classified_threads_needing_automation(self) -> List[Dict[str, Any]]:
        """Retrieve campaign threads with actionable intents."""
        intent_list = "', '".join(INTENT_TO_ACTION_MAP.keys())

        query = f"""
        SELECT c.campaign_thread_id,
               c.intent,
               c.created_at,
               c.updated_at,
               ct.status as thread_status
        FROM classifications c
        JOIN campaign_threads ct ON c.campaign_thread_id = ct.id
        WHERE c.intent IN ('{intent_list}')
          AND ct.status != 'automated_action_triggered'
        ORDER BY c.updated_at DESC;
        """

        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query)
            classified_threads = cursor.fetchall()

        logging.info(f"Found {len(classified_threads)} classified threads needing automation")
        return classified_threads

    def get_contact_info_for_thread(self, thread_id: str) -> Dict[str, str]:
        """Mock contact info retrieval. Replace with DB join in production."""
        mock_contacts = {
            "phone_number": "+1234567890",
            "email": "contact@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }

        logging.info(f"[MOCK] Retrieved contact info for thread {thread_id}")
        return mock_contacts

    def trigger_automated_action(self, thread_id: str, intent: str) -> bool:
        """Trigger the appropriate automated action for a given intent."""
        action = get_next_action_for_intent(intent)
        contact_info = self.get_contact_info_for_thread(thread_id)

        if action == "send_whatsapp":
            return self._send_whatsapp_follow_up(contact_info)
        elif action == "send_email":
            return self._send_email_follow_up(contact_info)

        logging.error(f"No action defined for intent '{intent}'")
        return False

    def _send_whatsapp_follow_up(self, contact_info: Dict[str, str]) -> bool:
        if not self.whatsapp_client:
            logging.error("WhatsApp client not configured")
            return False

        message = WhatsAppMessage(
            phone_number=contact_info["phone_number"],
            message_text=f"Hi {contact_info['first_name']}! Thanks for your interest. "
                         f"Here's the information you requested..."
        )
        return self.whatsapp_client.send_message(message)

    def _send_email_follow_up(self, contact_info: Dict[str, str]) -> bool:
        if not self.email_client:
            logging.error("Email client not configured")
            return False

        return self.email_client.send_email(
            recipient=contact_info["email"],
            subject="Follow-up from our conversation",
            body=f"Hi {contact_info['first_name']}, thanks for your time today..."
        )

    def mark_thread_as_processed(self, thread_id: str) -> None:
        """Update campaign_threads to reflect processed status."""
        update_query = """
        UPDATE campaign_threads
        SET status = 'automated_action_triggered', updated_at = NOW()
        WHERE id = %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(update_query, (thread_id,))
        self.connection.commit()

        logging.info(f"Marked thread {thread_id} as processed")