import heapq
import math
import sys

from Synopses.CM import CountMin


class CMTopK:
    class Element:
        def __init__(self, song_id, frequency):
            self.song_id = song_id
            self.frequency = frequency

        def __lt__(self, other):
            return self.frequency < other.frequency

    def __init__(self, k, epsilon, delta):
        width = math.ceil(math.e / epsilon)
        depth = math.ceil(math.log(1 / delta) / math.log(math.e))
        self.k = k
        self.cm = CountMin(width, depth)

        # Notice: provided solution usees array here. You can also use a minheap, this is provided in the commented code below.

        # self.min_heap = []
        self.topKArray = []
        self.top_k_set = set()
        # max int value
        self.minTopKArray = sys.maxsize

    def update(self, record):
        self.cm.update(record)
        song_id = record[2]
        if song_id in self.top_k_set:
            return

        estimate = self.cm.query(song_id)

        if len(self.topKArray) < self.k:
            self.top_k_set.add(song_id)
            self.topKArray.append(CMTopK.Element(song_id, estimate))
            self.minTopKArray = min(self.minTopKArray, estimate)
            return

        if estimate < self.minTopKArray:
            return

        indexOfMin = -1
        self.minTopKArray = sys.maxsize
        for i in range(len(self.topKArray)):
            self.topKArray[i].frequency = self.cm.query(self.topKArray[i].song_id)
            if self.topKArray[i].frequency < self.minTopKArray:
                self.minTopKArray = self.topKArray[i].frequency
                indexOfMin = i

        if estimate > self.minTopKArray:
            self.top_k_set.remove(self.topKArray[indexOfMin].song_id)
            self.topKArray[indexOfMin] = CMTopK.Element(song_id, estimate)
            self.top_k_set.add(song_id)

        #
        # if len(self.min_heap) < self.k:
        #     heapq.heappush(self.min_heap, CMTopK.Element(song_id, estimate))
        #     self.top_k_set.add(song_id)
        # else:
        #     if estimate > self.min_heap[0].frequency:
        #         self.update_heap()
        #         min_element = self.min_heap[0]
        #         if estimate > min_element.frequency:
        #             heapq.heappop(self.min_heap)
        #             self.top_k_set.remove(min_element.song_id)
        #             heapq.heappush(self.min_heap, CMTopK.Element(song_id, estimate))
        #             self.top_k_set.add(song_id)

    # def update_heap(self):
    #     new_heap = []
    #     while self.min_heap:
    #         e = heapq.heappop(self.min_heap)
    #         estimate = self.cm.query(e.song_id)
    #         heapq.heappush(new_heap, CMTopK.Element(e.song_id, estimate))
    #     self.min_heap = new_heap

    def query(self):
        answer = {}
        for e in self.topKArray:
            answer[e.song_id] = self.cm.query(e.song_id)
        #
        # for e in self.min_heap:
        #     answer[e.song_id] = self.cm.query(e.song_id)
        return answer
