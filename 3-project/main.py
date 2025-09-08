import logging
import psycopg2
from automation_runner import process_classified_threads_for_automation

import os
from dotenv import load_dotenv

load_dotenv()

def create_database_connection(connection_string: str):
    try:
        connection = psycopg2.connect(connection_string)
        logging.info("Database connection established")
        return connection
    except psycopg2.Error as db_error:
        logging.error(f"Database connection failed: {db_error}")
        raise

def main():
    db_connection_string = os.getenv("DB_CONNECTION_STR")
    USE_MOCK_CLIENTS = True

    logging.basicConfig(level=logging.INFO)

    connection = None
    try:
        connection = create_database_connection(db_connection_string)
        process_classified_threads_for_automation(connection, use_mock_clients=USE_MOCK_CLIENTS)
        logging.info("Automated next-step processing completed successfully")
    except Exception as error:
        logging.error(f"Automation failed: {error}")
        raise
    finally:
        if connection:
            connection.close()
            logging.info("Database connection closed")

if __name__ == "__main__":
    main()
