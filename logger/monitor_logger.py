import os
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import time


LOG_PATH = "logs"


def get_logger(name):
    logger = logging.getLogger(name)
    if os.path.exists(LOG_PATH):
        pass
    else:
        os.mkdir(LOG_PATH)
    # 设置日志基础级别
    logger.setLevel(logging.INFO)
    # 日志格式
    formatter = '%(asctime)s: %(levelname)s %(filename)s-%(module)s-%(funcName)s-%(lineno)d %(message)s'
    log_formatter = logging.Formatter(formatter)
    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    # info日志文件名
    info_file_name = 'info-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    # info日志处理器
    info_handler = TimedRotatingFileHandler(filename='logs/info/' + info_file_name, when='D', interval=1, backupCount=7,
                                            encoding='utf-8')
    info_handler.setFormatter(log_formatter)
    # error日志文件名
    error_file_name = 'error-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    # 错误日志处理器
    err_handler = TimedRotatingFileHandler(filename='logs/error/' + error_file_name, when='D', interval=1,
                                           backupCount=7, encoding='utf-8')
    err_handler.setFormatter(log_formatter)
    # 添加日志处理器
    logger.addHandler(info_handler)
    logger.addHandler(err_handler)
    logger.addHandler(console_handler)
    return logger
