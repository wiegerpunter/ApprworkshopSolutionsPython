import numpy as np
import hashlib
import mmh3


class CountMin:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        print("Width: ", width, "Depth: ", depth)
        self.cm = np.zeros((depth, width), dtype=int)

    def _hash(self, seed, value):
        return mmh3.hash(str(value), seed, False) % self.width

    def update(self, record):
        song_id = record[2]
        for i in range(self.depth):
            index = self._hash(i, song_id)
            self.cm[i][index] += 1

    def query(self, song_id):
        minest = float("inf")
        for i in range(self.depth):
            index = self._hash(i, song_id)
            minest = min(minest, self.cm[i][index])

        return minest

    def reset(self):
        self.cm.fill(0)
