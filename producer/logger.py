import logging
from pathlib import Path
from datetime import datetime


class Logger:
    logging_levels = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

    def __init__(self, log_dir: str = None, log_name: str = __name__, logging_level: str = 'INFO'):
        log_dir = Path(log_dir) / datetime.now().strftime(r'%y%m%d%H%M')
        if not log_dir.exists():
            log_dir.mkdir(parents=True)

        assert logging_level in self.logging_levels, f'Logging level: {logging_level} not found in mandatory levels {self.logging_levels}'
        self.logging_level = logging_level

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.getLevelName(logging_level))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
        file_handler = logging.FileHandler(str(log_dir.joinpath(f'{log_name}.log')))
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()  # if we want to print to consol
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
    
    def logInfo(self, msg: str) -> None:
        self.logger.info(msg)

    def logError(self, msg: str) -> None:
        self.logger.error(msg)

    def logWarning(self, msg: str) -> None:
        self.logger.warning(msg)
    
    def logDebug(self, msg: str) -> None:
        self.logger.debug(msg)
    
    def logCritical(self, msg: str) -> None:
        self.logger.critical(msg)


if __name__ == "__main__":
    logger = Logger(log_dir='logger', log_name='haha', logging_level='INFO')
    logger.logInfo('logInfo')
    logger.logError('logError')
    logger.logWarning('logWarning')
    logger.logDebug('logDebug')
    logger.logCritical('logCritical')
