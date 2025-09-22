import logging
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Use env values if available, else fallback to defaults
LOGS_PATH = os.getenv("LOGS_PATH", "logs")
LOGS_TEST_FILE = os.getenv("LOGS_TEST_FILE", "TEST.log")

# Ensure the logs folder exists (important for Render)
os.makedirs(LOGS_PATH, exist_ok=True)

class Logger:
    def __init__(self):
        self.logs_path = LOGS_PATH
        self.__setupLogging__()

    def __setupLogging__(self):
        log_file = os.path.join(self.logs_path, LOGS_TEST_FILE)

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(message)s",
        )

        # Silence noisy libs
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)

    def __getGMTOffset__(self):
        offset_minutes = datetime.now().astimezone().utcoffset().total_seconds() / 60
        hours = int(offset_minutes // 60)
        minutes = int(offset_minutes % 60)
        return f"GMT{hours:+02}:{minutes:02}"

    def logEvent(self, msg_creator, msg, uid=None, cid=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + self.__getGMTOffset__()

        if msg_creator == "USER":
            log_message = f"[{timestamp}] | --> [{msg_creator}:{uid}:{cid}]: {msg}"
        elif msg_creator == "RESP":
            log_message = f"[{timestamp}] | --> [{msg_creator}:{cid}]: {msg}"
        else:
            log_message = f"[{timestamp}] | [{msg_creator}]: {msg}"

        logging.info(log_message)
