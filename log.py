import logging

log_level = logging.INFO


logging.basicConfig(filename='c4.log',level=log_level)

def error(message):
    logging.error(message)

def warning(message):
    logging.warning(message)

def info(message):
    logging.info(message)

def debug(message):
    logging.debug(message)
