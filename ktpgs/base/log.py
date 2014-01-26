import logging
import tempfile

class GameLog(object):
    def __init__(self):
        if __debug__:
            _, tempname = tempfile.mkstemp(prefix='ketpe_',suffix='.log')
            logging.basicConfig(filename =tempname)
            logger = logging.getLogger("log1")
            logger.setLevel(logging.DEBUG)
            self._logger = logger

    @property
    def log(self):
        pass

    @log.setter
    def log(self,value):
        if __debug__:
            self._logger.debug(value)

