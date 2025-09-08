import logging
from factory import create_whatsapp_client, create_email_client
from automation_logic import VoiceCallProcessor, should_process_intent, get_next_action_for_intent

def process_classified_threads_for_automation(db_connection, use_mock_clients: bool = True) -> None:
    whatsapp_client = create_whatsapp_client(use_mock=use_mock_clients, mock_config={'should_fail': False, 'delay_seconds': 1})
    email_client = create_email_client(use_mock=use_mock_clients, mock_config={'should_fail': False})
    
    processor = VoiceCallProcessor(db_connection, whatsapp_client, email_client)
    classified_threads = processor.get_classified_threads_needing_automation()
    
    if not classified_threads:
        logging.info("No classified threads requiring automation found")
        return

    processed_count = 0
    failed_count = 0

    for classification in classified_threads:
        thread_id = classification['campaign_thread_id']
        intent = classification['intent']
        next_action = get_next_action_for_intent(intent)

        if should_process_intent(intent):
            action_successful = processor.trigger_automated_action(thread_id, intent)
            if action_successful:
                processor.mark_thread_as_processed(thread_id)
                processed_count += 1
                logging.info(f"Successfully triggered {next_action} for thread {thread_id}")
            else:
                failed_count += 1
                logging.error(f"Failed to trigger {next_action} for thread {thread_id}")

    logging.info(f"Automation complete: {processed_count} successful, {failed_count} failed")

    if use_mock_clients and hasattr(whatsapp_client, 'get_sent_messages'):
        logging.info(f"Mock WhatsApp messages sent: {len(whatsapp_client.get_sent_messages())}")
    if use_mock_clients and hasattr(email_client, 'get_sent_emails'):
        logging.info(f"Mock emails sent: {len(email_client.get_sent_emails())}")
