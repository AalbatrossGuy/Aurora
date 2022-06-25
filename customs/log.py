import logging
loggers = {}


def AuroraLogger(name: str, log_file: str):
    LOG_FILE = log_file
    global loggers

    if loggers.get(name):
        return loggers.get(name)
    else:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                                      datefmt="%d-%b-%y %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        loggers[name] = logger

        return logger
