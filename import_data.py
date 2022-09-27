from array import array
import os
from unittest import result
import numpy as np
cwd = os.getcwd()
files = os.listdir(cwd)

def init():
    global dis_mat
 
def compute_dis_mat(num_city, location):
    dis_mat = np.zeros((num_city, num_city))
    for i in range(num_city):
        for j in range(num_city):
            if i == j:
                dis_mat[i][j] = np.inf
                continue
            a = location[i]
            b = location[j]
            tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
            dis_mat[i][j] = tmp
    return dis_mat

    # def compute_pathlen(self, path, dis_mat):
    #     a = path[0]
    #     b = path[-1]
    #     result = dis_mat[a][b]
    #     for i in range(len(path) - 1):
    #         a = path[i]
    #         b = path[i + 1]
    #         result += dis_mat[a][b]
    #     return result

    # # 计算一个群体的长度
    # def compute_paths(self, paths):
    #     result = []
    #     for one in paths:
    #         length = self.compute_pathlen(one, self.dis_mat)
    #         result.append(length)
    #     return result

# def compute_paths(paths):
#     # for one in paths:
#     length = compute_pathlen(paths, dis_mat)
#     return length
def compute_pathlen(path, dis_mat):
    # length = compute_pathlen(paths, dis_mat)
    # a = path[0]
    # b = path[1]
    # result = dis_mat[a][b]
    # print(a)
    # print(b)
    # print(result)
    result = np.array([])
    lengths = np.array([])
    # print(result)
    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]
        length = dis_mat[a][b]
        lengths = np.save(result, length)
    print(lengths)

def read_tsp(path):
    lines = open(path, 'r').readlines()
    assert 'NODE_COORD_SECTION\n' in lines
    index = lines.index('NODE_COORD_SECTION\n')
    data = lines[index + 1:-1]
    tmp = []
    for line in data:
        line = line.strip().split(' ')
        if line[0] == 'EOF':
            continue
        tmpline = []
        for x in line:
            if x == '':
                continue
            else:
                tmpline.append(float(x))
        if tmpline == []:
            continue
        tmp.append(tmpline)
    data = tmp
    return data

data = read_tsp('optiseek/TSPLIB95/tsp/burma14.tsp')
data = np.array(data)
data = data[:, 1:]
dis_mat = compute_dis_mat(num_city=data.shape[0], location=data)
particals = np.array([13, 2, 3, 4, 5, 11, 6, 12, 7, 10, 8, 9, 0, 1])
path = np.insert(particals, len(particals+1), particals[0], axis = 0)
lenths = compute_pathlen(path, dis_mat)
print(lenths)