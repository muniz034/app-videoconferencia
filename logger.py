import datetime

class Logger:

    @staticmethod
    def format(message):
        return f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}"
    
    @staticmethod
    def debug(message):
        return print(Logger.format(message))