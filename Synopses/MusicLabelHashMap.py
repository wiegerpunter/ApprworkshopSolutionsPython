from Synopses.FM import FM


class MusicLabelHashMap:
    def __init__(self, epsilon, delta):
        self.epsilon = epsilon
        self.delta = delta
        self.map = {}

    def update(self, record):
        label = record[4]
        if label not in self.map:
            self.map[label] = FM(self.epsilon, self.delta)
        self.map[label].update(record)

    def query(self, label):
        return self.map[label].query() if label in self.map else 0

    def reset(self):
        self.map.clear()
