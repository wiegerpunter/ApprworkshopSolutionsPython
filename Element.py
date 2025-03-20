class Element:
    def __init__(self, song_id, frequency):
        self.song_id = song_id
        self.frequency = frequency

    def __lt__(self, other):
        return self.frequency < other.frequency

    def to_string(self):
        return str(self.song_id) + " " + str(self.frequency)