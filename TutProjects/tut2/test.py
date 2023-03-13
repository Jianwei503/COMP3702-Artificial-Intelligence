def two_d_array():
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[1, 2, 3], [4, 5, 6]]
    return a == b

def eq():
    return ('a' == 'a') \
           and (2 == 2) \
           and ([2,6] == [2,3])

if __name__ == "__main__":
    print(eq())