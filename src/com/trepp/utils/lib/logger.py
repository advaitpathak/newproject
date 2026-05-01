"""
This module implements a basic logger format and initializes a logger than can be used.
"""
import logging
import sys

APP_LOGGER_NAME = 'trepp-stream'


def get_logger(module_name):
    """
    Returns the logger for the child modules so that it shows up as datalake-sftp.lib.module_name
    :param module_name:
    :return: logger for module
    """
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)


def initiate_logger(logger_name = APP_LOGGER_NAME, logger_level_name='INFO', file_name=None):
    """
    Initates a logger with a basic format
    :param logger_name: sets top level logger name
    :param logger_level_name: DEBUG, INFO, etc
    :param file_name: local_file_name to use, on AWS it will write to cloudwatch
    :return:
    """
    logger = logging.getLogger(logger_name)
    logger.propagate = False
    logger.setLevel(logging.getLevelName(logger_level_name))
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(stream_handler)

    if file_name:
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
