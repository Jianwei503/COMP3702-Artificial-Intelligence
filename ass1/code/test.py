class A:
    def __init__(self, l=[]): #function call by reference
        self.l = l

def main():
    l = [[1, 2], [3, 4]]
    a = A(l)

    print(a.l)
    print(l)
    a.l.append([5, 6])
    print(a.l)
    print(l)

if __name__ == '__main__':
    main()