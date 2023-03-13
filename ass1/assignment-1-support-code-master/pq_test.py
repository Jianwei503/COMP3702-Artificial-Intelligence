import heapq

def pq_test():
    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, (1, 3))
    heapq.heappush(pq, (1, 2))
    heapq.heappush(pq, (1, 4))
    heapq.heappush(pq, (2, (0,0)))
    heapq.heappush(pq, (3, 'K'))
    heapq.heappush(pq, (4, 'G'))
    heapq.heappush(pq, (3, 'A'))
    heapq.heappush(pq, (0, {0:'X'}))

    while pq:
        n = heapq.heappop(pq)
        print(n)

class Obj:
    def __init__(self, v):
        self.v = v
    def __lt__(self, other):
        return self.v < other.v

def obj_test():
    pq = []
    heapq.heappush(pq, (9, Obj(2)))
    heapq.heappush(pq, (3, Obj(4)))
    heapq.heappush(pq, (3, Obj(0)))

    while pq:
        n = heapq.heappop(pq)
        print(n[1].v)

if __name__ == '__main__':
    # pq_test()
    obj_test()