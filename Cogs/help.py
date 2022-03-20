import interactions, logging
from datetime import datetime

# LOG SETTINGS
logger = logging.getLogger("auroralog")
logger.setLevel(logging.INFO)
LOG_FILE = 'logs/info.log'
fileHandler = logging.FileHandler(LOG_FILE)
fileHandler.setLevel(logging.INFO)
LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
fileHandler.setFormatter(LOG_FORMAT)
logger.addHandler(fileHandler)

error_logger = logging.getLogger("error-logger")
error_logger.setLevel(logging.DEBUG)
ERROR_LOG_FILE = '././logs/errors.log'
fileErrorHandler = logging.FileHandler(ERROR_LOG_FILE)
fileErrorHandler.setLevel(logging.DEBUG)
ERROR_LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
fileErrorHandler.setFormatter(ERROR_LOG_FORMAT)
error_logger.addHandler(fileErrorHandler)

# COMMANDS
class Help(interactions.Extension):
    def __init__(self, client):
        self.client = client



def setup(client):
    Help(client)
