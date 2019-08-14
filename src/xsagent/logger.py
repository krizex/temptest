import logging
import os


class Logger(object):
    def __init__(self, lvl, name):
        root_logger = logging.getLogger()
        root_logger.setLevel(lvl)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(lvl)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)-8s - [Thread-%(threadName)s]: %(message)s", "%Y-%m-%d %H:%M:%S")

        term_handler = logging.StreamHandler()
        term_handler.setFormatter(formatter)
        root_logger.addHandler(term_handler)
