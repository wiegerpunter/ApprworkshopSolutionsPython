import mmh3
import numpy as np
import hashlib
from collections import defaultdict, Counter
from scipy.stats import zipf


def _hash_value(seed, value, domain):
    # hash_obj = hashlib.md5(f"{seed}{value}".encode())

    return mmh3.hash(str(value), seed, False) % domain
    # return abs(int(hash_obj.hexdigest(), 16)) % domain


def get_user_engagement_per_label_approximate(syn, label):
    return syn.query(label)


class DataGeneration:
    def __init__(self, size, num_users, num_songs, num_artists, num_labels):
        self.size = size
        self.num_users = num_users
        self.num_songs = num_songs
        self.num_artists = num_artists
        self.num_labels = num_labels
        self.data = np.zeros((size, 5), dtype=int)

        self.zipf_user_id = zipf(a=1.001)
        self.zipf_song_id = zipf(a=1.8)
        self.zipf_artist_id = zipf(a=1.1)
        self.zipf_label_id = zipf(a=1.7)

        self.labels = set()

    def generate_data_exact(self):
        for i in range(self.size):
            self.data[i] = self._generate_row(i)

    def plot_distributions(self):
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.hist(self.data[:, 1], bins=50, color='blue', alpha=0.7)
        plt.title('User ID Distribution')
        plt.xlabel('User ID')
        plt.ylabel('Frequency')

        plt.subplot(2, 2, 2)
        plt.hist(self.data[:, 2], bins=50, color='orange', alpha=0.7)
        plt.title('Song ID Distribution')
        plt.xlabel('Song ID')
        plt.ylabel('Frequency')

        plt.subplot(2, 2, 3)
        plt.hist(self.data[:, 3], bins=50, color='green', alpha=0.7)
        plt.title('Artist ID Distribution')
        plt.xlabel('Artist ID')
        plt.ylabel('Frequency')

        plt.subplot(2, 2, 4)
        plt.hist(self.data[:, 4], bins=50, color='red', alpha=0.7)
        plt.title('Label ID Distribution')
        plt.xlabel('Label ID')
        plt.ylabel('Frequency')

        plt.tight_layout()
        plt.show()


    def ingest_data_into_sketch(self, sketch):
        for row in self.data:
            sketch.update(row)

    def _generate_row(self, i):
        record = np.zeros(5, dtype=int)
        record[0] = i
        record[1] = _hash_value(1, self.zipf_user_id.rvs(size=1)[0], self.num_users)
        record[2] = _hash_value(2, self.zipf_song_id.rvs(size=1)[0], self.num_songs)
        record[3] = _hash_value(3, self.zipf_artist_id.rvs(size=1)[0], self.num_artists)
        record[4] = _hash_value(4, self.zipf_label_id.rvs(size=1)[0], self.num_labels)
        self.labels.add(record[4])
        return record

    def get_user_engagement_per_label_exact(self):
        unique_user_song_pairs_per_label = defaultdict(set)
        for row in self.data:
            label = row[4]
            unique_user_song_pairs_per_label[label].add((row[1], row[2]))

        return {label: len(pairs) for label, pairs in unique_user_song_pairs_per_label.items()}

    def get_top_songs_exact(self, K):
        answer = {}
        song_counts = Counter(self.data[:, 2])
        top_songs = song_counts.most_common(K)

        for song, count in top_songs:
            answer[song] = count

        return answer
