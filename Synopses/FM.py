import numpy as np
import hashlib
import math
import mmh3


def _hash(seed, song_id, user_id):
    hash_key = (song_id * 0x1F1F1F1F) ^ (user_id * 0x7F7F7F7F)
    return mmh3.hash64(hash_key, seed, signed=False)[0]
    #
    # hash_obj = hashlib.md5(f"{seed}{hash_key}".encode())
    # return int(hash_obj.hexdigest(), 16) % (2**31)


class FM:
    def __init__(self, epsilon, delta):
        num_hashes = math.ceil(math.log(1 / delta) / math.log(2) / (epsilon ** 2))
        print("Num hashes: ", num_hashes)
        self.bitmap_size = 64
        self.sketch = np.zeros((num_hashes, self.bitmap_size), dtype=bool)

    # def _lsb(self, value):
    #     rho = 0
    #     while rho < self.bitmap_size and (value & 0x01) == 0:
    #         value >>= 1
    #         rho += 1
    #     return rho if rho < self.bitmap_size else 0

    def _lsb(self, value):
        return (value & -value).bit_length() - 1  # Faster way to get the position of the least significant bit

    def update(self, record):
        song_id, user_id = record[1], record[2]
        for i in range(len(self.sketch)):
            hash_val = _hash(i, song_id, user_id)
            self.sketch[i][self._lsb(hash_val)] = True

    def query(self):
        R = []
        for i in range(len(self.sketch)):
            rho = next((j for j in range(self.bitmap_size) if not self.sketch[i][j]), self.bitmap_size)
            R.append(rho)

        constant = 1.2928
        avg_R = sum(R) / len(R)
        return int(math.pow(2, avg_R) * constant)

    def reset(self):
        self.sketch.fill(False)
