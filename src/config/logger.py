import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Временно для отладки

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
