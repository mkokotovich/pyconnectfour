import logging
logging.basicConfig(filename='c4.log',level=logging.DEBUG)

def error(message):
    logging.error(message)

def warning(message):
    logging.warning(message)

def info(message):
    logging.info(message)

def debug(message):
    logging.debug(message)
