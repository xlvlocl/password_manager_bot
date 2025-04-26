import logging
from telebot import logger as telebot_logger


class CustomColorFormatter(logging.Formatter):
    COLOR_TIME = "\x1b[38;5;240m"
    COLOR_FILE = "\x1b[38;5;33m"
    COLOR_FUNC = "\x1b[38;5;246m"
    COLOR_LINE = "\x1b[38;5;245m"
    COLOR_SEP = "\x1b[38;5;240m"

    COLOR_LEVEL = {
        logging.DEBUG: "\x1b[38;5;37m",
        logging.INFO: "\x1b[38;5;34m",
        logging.WARNING: "\x1b[38;5;220m",
        logging.ERROR: "\x1b[38;5;196m",
        logging.CRITICAL: "\x1b[1;31m",
        }

    COLOR_MESSAGE = {
        logging.DEBUG: "\x1b[38;5;250m",
        logging.INFO: "\x1b[38;5;255m",
        logging.WARNING: "\x1b[38;5;226m",
        logging.ERROR: "\x1b[38;5;203m",
        logging.CRITICAL: "\x1b[1;31m",
        }

    RESET = "\x1b[0m"

    def format(self, record):
        color_level = self.COLOR_LEVEL.get(record.levelno, self.RESET)
        color_message = self.COLOR_MESSAGE.get(record.levelno, self.RESET)

        time_part = f"{self.COLOR_TIME}{self.formatTime(record, self.datefmt)}{self.RESET}"
        file_part = f"{self.COLOR_FILE}{record.filename}{self.RESET}"
        func_part = f"{self.COLOR_FUNC}{record.funcName}{self.RESET}"
        line_part = f"{self.COLOR_LINE}{record.lineno}{self.RESET}"
        sep_part = f"{self.COLOR_SEP} - {self.RESET}"
        level_part = f"{color_level}{record.levelname}{self.RESET}"
        message_part = f"{color_message}{record.getMessage()}{self.RESET}"

        return (
            f"{time_part} {file_part}({func_part} - {line_part}){sep_part} {level_part}{sep_part} {message_part}"
        )


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(CustomColorFormatter(datefmt='%y.%d.%m'))
    logger.addHandler(handler)

    return logger


for handler in telebot_logger.handlers[:]:
    telebot_logger.removeHandler(handler)

handler = logging.StreamHandler()
handler.setFormatter(CustomColorFormatter(datefmt='%y.%d.%m'))
telebot_logger.addHandler(handler)
