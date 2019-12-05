from os import name
from utility import check_os_path
from datetime import datetime

import view


def is_win() -> bool:
    """ Return True if OS is Windows """
    return True if name == "nt" else False


class Logging(object):
    instance = None

    def __new__(self):
        if not self.instance:
            self.instance = super(Logging, self).__new__(self)
            self.subscribers = dict()
        return self.instance

    def register(self, who, callback=None):
        if callback is None:
            callback = getattr(who, 'update_view')
        self.subscribers[who] = callback

    def unregister(self, who):
        del self.subscribers[who]

    def dispatch(self, message):
        for subscriber, callback in self.subscribers.items():
            callback(message)


class Log_subcriber(object):
    def __init__(self, name):
        self.name = name

    def update_view(self, message):
        view.update_logger_label(message)

    def save_to_file(self, message):
        print('Saving to file ' + message)
        filepath = 'logs{path}{filename}'.format(path=check_os_path(), filename='log.txt')
        try:
            with open(filepath, "a+") as file:
                file.write('{datetime} -- {message}\n'.format(datetime=datetime.now(), message=message))
        except:
            pass