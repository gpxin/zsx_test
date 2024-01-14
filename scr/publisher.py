class Publisher:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        pass

    def remove(self, observer):
        pass

    def notify_obs(self):
        [obs.notify(self) for obs in self.observers]