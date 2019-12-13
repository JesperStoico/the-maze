class Logging(object):
    instance = None

    def __new__(self):
        if not self.instance:
            self.instance = super(Logging, self).__new__(self)
            self.subscribers = list()
        return self.instance

    def register(self, who):
        self.subscribers.append(who)

    def unregister(self, who):
        del self.subscribers[who]

    def dispatch(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)


class Log_subcriber(object):
    def __init__(self, name, method):
        self.name = name
        self.method = method

    def update(self, message):
        self.method(message)
