from datetime import datetime

from Data.DataGeneration import DataGeneration
from Synopses.CMTopK import CMTopK
from Synopses.MusicLabelHashMap import MusicLabelHashMap


def compare_exact_approx(topk_exact, topk_appr):
    # see how many of appr topk are in exact topk

    # print the appr topk
    print("Approximate top K")
    for song in topk_appr:
        print(song, topk_appr[song])

    for song in topk_exact:
        print(song, topk_exact[song])
        if song not in topk_appr:
            print(f"SongID: {song} Error: not in approximate top K")
        else:
            print(f"SongID: {song} Error: {abs(topk_exact[song] - topk_appr[song]) / topk_exact[song]}")


def question2(data):
    print("Question 2")
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
    data.generate_data_approximate(sketch)
    time = datetime.now()
    topk_appr = sketch.query()
    print("Appr. Query time: ", datetime.now() - time)
    print("\n")
    compare_exact_approx(topk_exact, topk_appr)


def question1(data):
    print("Question 1")
    print("User engagement per label:")
    time = datetime.now()
    exact = data.get_user_engagement_per_label_exact()
    for label in data.labels:
        print(f"Label: {label} has {exact[label]} unique user-song pairs.")
    print("Exact Query time: ", datetime.now() - time)
    print("\n")

    epsilon = 0.1
    delta = 0.1
    sketch = MusicLabelHashMap(epsilon, delta)
    print("Approximate data insertion")
    time = datetime.now()
    data.generate_data_approximate(sketch)
    print("Time taken: ", datetime.now() - time)
    print("User engagement per label (approximate):")
    time = datetime.now()
    for label in data.labels:
        estimate = sketch.query(label)
        print(f"Label: {label} has {estimate} unique user-song pairs.")
        print("Error: ", abs(exact.get(label) - estimate) / exact.get(label))

    print("Appr. Query time: ", datetime.now() - time)


def run():
    size = int(1e6)
    numUsers = int(18e6)
    numSongs = int(100e6)
    numArtists = int(1e6)
    numLabels = int(20)

    data = DataGeneration(size, numUsers, numSongs, numArtists, numLabels)
    data.generate_data_exact()

    # question 1
    question1(data)

    # question 2
    question2(data)


run()
