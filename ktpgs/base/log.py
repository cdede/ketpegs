import logging
import tempfile

class GameLog(object):
    def __init__(self, _is_debug ,work_path):
        self._is_debug = _is_debug
        if self._is_debug:
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
        if self._is_debug:
            self._logger.debug(value)


