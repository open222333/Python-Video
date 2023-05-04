from . import LOG_PATH, LOG_LEVEL, LOG_DISABLE, LOG_FILE_DISABLE, LOG_SIZE, LOG_DAYS
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from traceback import print_exc
from datetime import datetime
import logging
import socket
import os


'''
; ******log設定******
; 關閉log功能 輸入選項 (true, True, 1) 預設 不關閉
; LOG_DISABLE=1

; logs路徑 預設 logs
; LOG_PATH=

; 關閉紀錄log檔案 輸入選項 (true, True, 1)  預設 不關閉
; LOG_FILE_DISABLE=1

; 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
; LOG_LEVEL=

; 指定log大小(輸入數字) 單位byte, 與 LOG_DAYS 只能輸入一項 若都輸入 LOG_SIZE優先
; LOG_SIZE=

; 指定保留log天數(輸入數字) 預設7
; LOG_DAYS=
'''


class Log():

    def __init__(self, log_name: str) -> None:
        self.log_name = log_name
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.WARNING)

        # 當前日期
        self.now_time = datetime.now().__format__('%Y-%m-%d')

        self.log_path = 'logs'
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        self.log_file = os.path.join(self.log_path, f'{log_name}-all.log')
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def set_log_path(self, log_path: str):
        """設置log檔存放位置

        Args:
            log_path (str): 路徑 預設為 logs
        """
        self.log_path = log_path
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

    def set_log_file_name(self, name: str):
        """設置log檔名稱 預設為 {log_name}-all.log

        Args:
            name (str): _description_
        """
        self.log_file = os.path.join(self.log_path, name)

    def set_date_handler(self, days: int = 7) -> TimedRotatingFileHandler:
        """設置每日log檔

        Args:
            log_file (_type_): log檔名
            days (int, optional): 保留天數. Defaults to 7.

        Returns:
            TimedRotatingFileHandler: _description_
        """
        self.log_file = os.path.join(self.log_path, f'{self.log_name}-{self.now_time}.log')
        handler = TimedRotatingFileHandler(self.log_file, when='D', backupCount=days)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def set_file_handler(self, size: int = 1 * 1024 * 1024, file_amount: int = 5) -> RotatingFileHandler:
        """設置log檔案大小限制

        Args:
            log_file (_type_): log檔名
            size (int, optional): 檔案大小. Defaults to 1*1024*1024 (1M).
            file_amount (int, optional): 檔案數量. Defaults to 5.

        Returns:
            RotatingFileHandler: _description_
        """
        handler = RotatingFileHandler(self.log_file, maxBytes=size, backupCount=file_amount)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def set_msg_handler(self) -> logging.StreamHandler:
        """設置log steam

        Returns:
            logging.StreamHandler: _description_
        """
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def set_log_formatter(self, formatter: str):
        """設置log格式 formatter

        %(asctime)s - %(name)s - %(levelname)s - %(message)s

        Args:
            formatter (str): log格式.
        """
        self.formatter = logging.Formatter(formatter)

    def set_level(self, level: str = 'WARNING'):
        """設置log等級

        Args:
            level (str): 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
        """
        if level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif level == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
            self.logger.setLevel(logging.CRITICAL)

    def debug(self, message: str, exc_info: bool = False):
        self.logger.debug(message, exc_info=exc_info)

    def info(self, message: str, exc_info: bool = False):
        self.logger.info(message, exc_info=exc_info)

    def warning(self, message: str, exc_info: bool = False):
        self.logger.warning(message, exc_info=exc_info)

    def error(self, message: str, exc_info: bool = False):
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False):
        self.logger.critical(message, exc_info=exc_info)


try:
    HOSTNAME = socket.gethostname()

    log_setting = {
        'LOG_PATH': LOG_PATH,
        'LOG_DISABLE': LOG_DISABLE,
        'LOG_FILE_DISABLE': LOG_FILE_DISABLE,
        'LOG_LEVEL': LOG_LEVEL,
        'LOG_SIZE': LOG_SIZE,
        'LOG_DAYS': LOG_DAYS
    }
except Exception as err:
    print_exc()

# 建立log資料夾
if not os.path.exists(LOG_PATH) and not LOG_DISABLE:
    os.makedirs(LOG_PATH)

if LOG_DISABLE:
    logging.disable()
else:
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if LOG_SIZE:
        log_file = f'{LOG_PATH}/{HOSTNAME}-mega.log'
        if not LOG_FILE_DISABLE:
            log_file_handler = RotatingFileHandler(f'logs/{log_file}.log', maxBytes=LOG_SIZE, backupCount=5)
            log_file_handler.setFormatter(log_formatter)
    else:
        log_file = f'{LOG_PATH}/{datetime.now().__format__("%Y%m%d")}-{HOSTNAME}.log'
        if not LOG_FILE_DISABLE:
            log_file_handler = TimedRotatingFileHandler(log_file, when='D', backupCount=LOG_DAYS)
            log_file_handler.setFormatter(log_formatter)

    log_msg_handler = logging.StreamHandler()
    log_msg_handler.setFormatter(log_formatter)

    logger = logging.getLogger(HOSTNAME)

    if LOG_LEVEL == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif LOG_LEVEL == 'INFO':
        logger.setLevel(logging.INFO)
    elif LOG_LEVEL == 'WARNING':
        logger.setLevel(logging.WARNING)
    elif LOG_LEVEL == 'ERROR':
        logger.setLevel(logging.ERROR)
    elif LOG_LEVEL == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)

    if not LOG_FILE_DISABLE:
        logger.addHandler(log_file_handler)
    logger.addHandler(log_msg_handler)

    logger.debug(log_setting)
