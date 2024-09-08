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
