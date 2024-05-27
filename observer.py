class Subject:
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def notify(self, value):
        for observer in self._observers:
            observer.update(value)

class Observer:
    def update(self, subject):
        pass