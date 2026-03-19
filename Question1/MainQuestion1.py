from datetime import datetime

from Data.DataGeneration import DataGeneration
from Question1.CMTopK import CMTopK


def compare_exact_approx(topk_exact, topk_appr):
    # see how many of appr topk are in exact topk

    # print the appr topk
    print("Approximate top K")
    for song in topk_appr:
        print(song, topk_appr[song])

    for song in topk_exact:
        if song not in topk_appr:
            print(f"SongID: {song} Error: not in approximate top K")
        else:
            print(f"SongID: {song} Error: {abs(topk_exact[song] - topk_appr[song]) / topk_exact[song]}")


def question1(data):
    print("Question 1")
    """
    For this question, we need to find the top K songs that have the highest frequency in the dataset, as well as their frequency.
    We will compare the exact and approximate results.
    """

    K = 10
    time = datetime.now()
    topk_exact = data.get_top_songs_exact(K)
    print("Exact Query time: ", datetime.now() - time)
    print("\n")
    epsilon = 0.01
    delta = 0.01
    sketch = CMTopK(K, epsilon, delta)
    time = datetime.now()
    data.ingest_data_into_sketch(sketch)
    print("Ingestion time taken: ", datetime.now() - time)
    time = datetime.now()
    topk_appr = sketch.query()
    print("Appr. Query time: ", datetime.now() - time)
    print("\n")
    compare_exact_approx(topk_exact, topk_appr)


def run():
    size = int(100000)
    numUsers = int(18e6)
    numSongs = int(100e6)
    numArtists = int(1e6)
    numLabels = int(20)
    time = datetime.now()
    data = DataGeneration(size, numUsers, numSongs, numArtists, numLabels)
    data.generate_data_exact()
    print("Data generated, size: ", size, ". Time taken: ", datetime.now() - time)
    # question 1
    question1(data)


run()