import logging
import os
import time


class LogTool:
    # 初始化日志
    def __init__(self):
        self.logPath = os.getcwd()
        self.logName = f'{time.strftime("%Y%m%d%H%M", time.localtime(time.time()))}.log'
        self.logFile = self.logPath + self.logName
        # 日志的输出格式
        logging.basicConfig(
            level=logging.DEBUG,  # 级别：CRITICAL > ERROR > WARNING > INFO > DEBUG，默认级别为 WARNING
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s:  %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=self.logFile,
            filemode='a')

    def debug(self, content):
        logging.debug(content)
        # 可以写其他的函数,使用其他级别的log

    def error(self, content):
        logging.error(content)

    def warning(self, content):
        logging.warning(content)

    def info(self, content):
        logging.info(content)
