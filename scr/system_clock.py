from scr.publisher import Publisher


class SystemClock(Publisher):
    def __init__(self):
        super().__init__()
        self.time = 0

    def notify_obs(self):
        [obs.notify(self) for obs in self.observers]
        self.time += 1
