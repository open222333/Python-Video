from configparser import ConfigParser
import os


conf = ConfigParser()
conf.read(os.path.join('conf', 'config.ini'), encoding='utf-8')


# logs相關參數
# 關閉log功能 輸入選項 (true, True, 1) 預設 不關閉
LOG_DISABLE = conf.getboolean('DEFAULT', 'LOG_DISABLE', fallback=False)
# logs路徑 預設 logs
LOG_PATH = conf.get('DEFAULT', 'LOG_PATH', fallback='logs')
# 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
LOG_LEVEL = conf.get('DEFAULT', 'LOG_LEVEL', fallback='WARNING')
# 關閉紀錄log檔案 輸入選項 (true, True, 1)  預設 不關閉
LOG_FILE_DISABLE = conf.getboolean('DEFAULT', 'LOG_FILE_DISABLE', fallback=False)
# 指定log大小(輸入數字) 單位byte, 與 LOG_DAYS 只能輸入一項 若都輸入 LOG_SIZE優先
LOG_SIZE = conf.getint('DEFAULT', 'LOG_SIZE', fallback=0)
# 指定保留log天數(輸入數字) 預設7
LOG_DAYS = conf.getint('DEFAULT', 'LOG_DAYS', fallback=7)

NGS_AVDATA_HOST = conf.get('HOST', 'NGS_AVDATA_HOST', fallback=None)

IG_USERNAME = conf.get('INSTAGRAM', 'USERNAME', fallback=None)
IG_PASSWORD = conf.get('INSTAGRAM', 'PASSWORD', fallback=None)
