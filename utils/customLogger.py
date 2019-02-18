import logging
import inspect


def custom_logger(log_level=logging.DEBUG):
    # step1: Create Logger object and set level
    '''
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    '''
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(name=logger_name)  # Log record object
    logger.setLevel(logging.DEBUG)

    # step2: Create Handler(console here) and set its log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # step3: Define formatter and add formatter to handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                                  datefmt='%m/%d/%Y %H:%M:%S')
    console_handler.setFormatter(fmt=formatter)

    # step4: Integrate Handler to Logger
    logger.addHandler(console_handler)

    return logger
