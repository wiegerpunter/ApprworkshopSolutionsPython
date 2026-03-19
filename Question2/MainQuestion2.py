from datetime import datetime

from Data.DataGeneration import DataGeneration
from Question2.MusicLabelHashMap import MusicLabelHashMap


def question2(data):
    print("Question 2")
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
    data.ingest_data_into_sketch(sketch)
    print("Ingestion time taken: ", datetime.now() - time)
    print("User engagement per label (approximate):")
    time = datetime.now()
    for label in data.labels:
        estimate = sketch.query(label)
        print(f"Label: {label} is estimated to have {estimate} unique user-song pairs. Exact: {exact[label]}"
              f", error: {round(abs(exact[label] - estimate) / exact[label], 3)}")
    print("Appr. Query time: ", datetime.now() - time)


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

    # question 2
    question2(data)


run()
