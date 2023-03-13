import queue

def main():
    pq = queue.PriorityQueue()
    pq.put(2)
    pq.put(1)
    pq.put(6)
    pq.put(0)
    pq.put(-1)
    pq.put(-10)

    while not pq.empty():
        print(pq.get())

if __name__ == '__main__':
    main()