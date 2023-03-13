import math

from angle import Angle
from tester import triangle_orientation


class A:
    def __init__(self, x, y, o):
        self.x = x
        self.y = y
        self.o = o
    def __lt__(self, other):
        return self.x + self.y < other.x + other.y
    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
        return hash((self.x, self.y)) == hash((other.x, other.y))
    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def set_v(self, x, y):
        self.x = x
        self.y = y

    def get_o(self):
        return self.o

class O:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __str__(self):
        return "({}, {})".format(self.a, self.b)
    def get_v(self):
        return (self.a, self.b)
    def set_v(self, a, b):
        self.a = a
        self.b = b



def arr_sort(list=[]):
    list.sort()
    for l in list:
        print((l.x, l.y))

def remove_last(list):
    list.pop()


def get_last_length_angle(point_a, point_b, point_c):
    edge_a = math.hypot(point_c[0] - point_b[0], point_c[1] - point_b[1])
    edge_b = math.hypot(point_c[0] - point_a[0], point_c[1] - point_a[1])
    edge_c = math.hypot(point_b[0] - point_a[0], point_b[1] - point_a[1])

    cos_b = (edge_a**2 + edge_c**2 - edge_b**2) / (2 * edge_a * edge_c)
    angle_b = Angle.acos(cos_b).in_degrees()
    last_angle = 180 - angle_b

    orientation = triangle_orientation(point_a, point_b, point_c)
    if orientation == 0:
        return edge_a, 0
    elif orientation > 0:
        return edge_a, last_angle
    else:
        return edge_a, last_angle * (-1)

def main():
    # arr = [A(4, 4), A(1, 1), A(3, 3), A(2, 2)]
    # for a in arr:
    #     print((a.x, a.y))
    #
    # print("**********************")
    #
    # # list = []
    # # list.extend(arr)
    # list = arr[:]
    # arr_sort(list)
    # print("******************")
    #
    # for a in arr:
    #     print((a.x, a.y))


    # s = set()
    # s.add(A(4, 4))
    # s.add(A(2, 2))
    # s.add(A(4, 4))
    #
    # for a in s:
    #     print((a.x, a.y))

    # for i in ['A', 'B', "C"]:
    #     print(i)
    #     for j in [1,2,3,4,5]:
    #         print(j)
    #         if j == 2:
    #             break

    # arr = [1,2,3,4,5]
    # remove_last(arr)
    # print(arr)

    # s = set("conn")
    # print(s)
    # s.add('m')
    # for c in s:
    #     print(c)
    # print(s)
    # s.discard('c')
    # print(s)

    # s = {A(1, 1), A(2, 2), A(3, 3), A(1, 1)}
    # for a in s:
    #     print(a)
    # # print(s)
    # print("*************")
    # x = s.intersection({A(2, 2)})
    # print(x)
    # print("************")
    # x.pop().set_v(22, 22)
    # print(x)
    # print("*********")
    # for a in s:
    #     print(a)



    # a = A(1, 1)
    # b = A(2, 2)
    # c = A(3, 3)
    # d = A(1, 1)
    #
    # dt = dict()
    # dt[A(1, 1)] = a
    # dt[A(2, 2)] = b
    # dt[A(3, 3)] = c
    # dt[A(1, 1)] = d
    #
    # for k in dt.keys():
    #     print("{}:{}".format(k, dt[k]))
    #
    # # o = dt[A(3, 3)]
    # # print(o)
    # # o.set_v(33, 33)
    # # print(o)
    #
    # vs = list(dt.values())
    # vs[0].set_v(11, 11)
    # vs[1].set_v(22, 22)
    # vs[2].set_v(33, 33)
    # vs.remove(A(11, 11))
    # for l in vs:
    #     print(l)
    #
    #
    # for k in dt.keys():
    #     print("{}:{}".format(k, dt[k]))



    # a = 0.326576
    # b = 5
    # c = a / b
    # print(c)


    # o1 = O('a', 'b')
    # a = A(1, 1, o1)
    # o2 = a.get_o()
    # o2.set_v('c', 'd')
    # print(o1)

    # A = (0, 0)
    # B = (1, 1)
    # C = (2, 0)
    #
    # len, ang = get_last_length_angle(A, B, C)
    # print((len, ang))


    for i in range(0, 5, 2):
        print(i)



if __name__ == '__main__':
    main()