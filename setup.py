""" app runner """
from answers_service import APP

if __name__ == '__main__':
    if not APP.debug:
        from logging.config import fileConfig

        fileConfig('logging.config')
    APP.run()
