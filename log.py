import logging
import atexit

DEBUG=5
INFO=4
WARNING=3
ERROR=2
CRITICAL=1

log_level = DEBUG
file_name = "c4.log"

log = open(file_name, "a")

def exit_logger():
    write_message("Closing log file")
    if log:
        log.flush()
        log.close()


atexit.register(exit_logger)


def write_message(message):
    log.write(message + "\n")


def error(message):
    if (log_level >= ERROR):
        write_message("ERROR: " + message)

def warning(message):
    if (log_level >= WARNING):
        write_message("WARNING: " + message)

def info(message):
    if (log_level >= INFO):
        write_message("INFO: " + message)

def debug(message):
    if (log_level >= DEBUG):
        write_message("DEBUG: " + message)
