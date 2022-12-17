"""
    MAIN FILE FOR LOGGER IMPLEMENTATION
"""
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

day = datetime.now().strftime("%d-%m-%Y-%H")

if not os.path.exists("app/Logs"):
    os.makedirs("app/Logs")

# create logger
logger = logging.getLogger("log")
logger.setLevel(level=logging.DEBUG)

# set formatter
logFileFormatter = logging.Formatter(
    fmt="%(levelname)s %(asctime)s \t %(pathname)s --> %("
    "funcName)s (Line %(lineno)s) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# set the handler
fileHandler = TimedRotatingFileHandler(
    filename=f"app/Logs/{day}:00_Project_Level.log",
    when="h",
    interval=1,
    backupCount=24,
)

fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.DEBUG)
logger.addHandler(fileHandler)
