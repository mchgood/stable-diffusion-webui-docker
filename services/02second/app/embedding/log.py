from loguru import logger


class LogUtil():

    @classmethod
    def init(cls):
        logger.add("../logs/{time:YYYY-MM-DD}.log", rotation="100 MB", retention="3 days", enqueue=True)
        return logger


log = LogUtil().init()
