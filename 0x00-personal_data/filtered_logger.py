#!/usr/bin/env python3

"""Log and filter data"""
import logging
from typing import List, Tuple
import os
import re
import mysql.connector


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscate the log message."""
    pattern = r"|".join([f"(?<={field}=)[^{separator}]+" for field in fields])
    return re.sub(pattern, redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Intialize."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format."""
        record.msg = filter_datum(self.fields,
                                  self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger object
    that obfuscates sensitive information.
    """

    # Create a logger with the name 'user_data'
    logger = logging.getLogger("user_data")

    # Set the logger level to INFO
    logger.setLevel(logging.INFO)

    # Ensure it does not propagate messages to other loggers
    logger.propagate = False

    # Create a StreamHandler for logging to the console
    handler = logging.StreamHandler()

    # Use the RedactingFormatter to format the logs and obfuscate PII fields
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQL database using credentials
    stored in environment variables."""

    # Retrieve database credentials from environment variables
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    passy = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    # Establish and return the connection to the database
    return mysql.connector.connection.MySQLConnection(
        user=username,
        password=passy,
        host=host,
        database=database
    )


def main():
    """Main function to retrieve and log user data from the database."""
    db = get_db()
    cursor = db.cursor()

    # Execute the query to retrieve all rows from the users table
    cursor.execute("SELECT * FROM users")

    # Get the column names (assuming the users table
    # columns match the PII_FIELDS)
    columns = [desc[0] for desc in cursor.description]

    logger = get_logger()

    # Iterate through each row in the result set
    for row in cursor.fetchall():
        # Create a dictionary mapping columns to values
        row_dict = dict(zip(columns, row))

        # Convert the dictionary to a log message string
        log_message = "; ".join(f"{key}={value}"
                                for key, value in row_dict.items()) + ";"

        # Log the message using the logger
        logger.info(log_message)

    # Close the cursor and database connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
