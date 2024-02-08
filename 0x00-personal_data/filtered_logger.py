#!/usr/bin/env python3
"""Use of regex in replacing occurences of certain field values
"""


import logging
import os
import mysql.connector
import re
from typing import List


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
# Tuple of PII fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns filtered values from log records"""
        # call the parent class's format method to get the formatted log line
        msg = super(RedactingFormatter, self).format(record)
        # use the filter_datum function to perform substitution of self.fields
        text = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return text


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
) -> str:
    """Returns regex obfuscated log messages"""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.propagate = False

    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connection to MYSQL environment"""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main() -> None:
    """obtain a database connection using get_db 
    and retrieve all rows in the users table and display 
    each row under a filtered format"""
    logger = get_logger()
    logger.setLevel(logging.INFO)

    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        message = "; ".join([f"{field}={row[field]}" for field in row.keys()])
        logger.info(filter_datum(PII_FIELDS, RedactingFormatter.REDACTION,
                                 message, RedactingFormatter.SEPARATOR))


if __name__ == "__main__":
    main()
