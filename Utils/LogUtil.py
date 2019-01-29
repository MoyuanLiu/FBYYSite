import logging
from logging.handlers import TimedRotatingFileHandler
import time
import re

def getcurloghandler(basefilename,when,interval,backupcount):
    currentdate = time.strftime("%Y.%m.%d", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(LOG_FORMAT)
    # 创建TimedRotatingFileHandler对象
    log_file_handler = TimedRotatingFileHandler(filename=basefilename+"-%s.log" % currentdate, when=when,interval=interval, backupCount=backupcount)
    log_file_handler.suffix = "%Y.%m.%d.log"
    log_file_handler.extMatch = re.compile(r"^\d{4}\.\d{2}\.\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.DEBUG)
    return log_file_handler