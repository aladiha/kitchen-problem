from collections import deque

visitedEmployees = dict()
visitedS = dict()
saveIndices = [0, 0]

# re define visited places for next iteration
def reDefineVisitedSpaces(rows, cols):
    global visitedS
    for i in range(rows):
        for j in range(cols):
            visitedS[(i, j)] = False

# re define visited Employees for next iteration
def reDefineVisitedEmployees():
    for key in visitedEmployees:
        visitedEmployees[key] = [False, 0]

#check if indecies out if range
def is_in_range(map_, i, j, rows, cols):
    if i < 0 or j < 0 or j >= cols or i >= rows or map_[i][j] == 'W':
        return False
    return True

#bfs search algo to find shortest path
def bfs(map_, i, j, rows, cols, sum_ = 0):
    pathI = [-1, 0, 1, 0]
    pathJ = [0, 1, 0, -1]

    q = deque()
    q.append([i, j, 0])
    visitedS[(i, j)] = True

    while (len(q) > 0):
        temp = q.popleft()
        i = temp[0]
        j = temp[1]
        level = temp[2]

        if map_[i][j] == 'E' and not visitedEmployees[(i, j)][0]:
            visitedEmployees[(i, j)][0] = True
            visitedEmployees[(i, j)][1] = level
            i = saveIndices[0]
            j = saveIndices[1]
            level = 0
            reDefineVisitedSpaces(rows, cols)
            q = deque()
            visitedS[(i, j)] = True

        for k in range(4):
            if is_in_range(map_, i+pathI[k], j+pathJ[k], rows, cols) and not visitedS[(i+pathI[k], j+pathJ[k])]:
                visitedS[(i + pathI[k], j + pathJ[k])] = True
                q.append([i + pathI[k], j + pathJ[k], level + 1])

# for every possible kitchen location run bfs algo
def find_path(map_, rows, cols):
    location = []
    min_sum = float('inf')
    global saveIndices
    global visitedEmployees
    for i in range(rows):
        for j in range(cols):
            if map_[i][j] == 'E':
                visitedEmployees[(i, j)] = [False, 0]
            visitedS[(i, j)] = False

    for i in range(rows):
        for j in range(cols):
            newSum = 0
            flag = 1
            if map_[i][j] == ' ':
                visitedS[(i, j)] = True
                saveIndices = [i, j]
                bfs(map_, i, j, rows, cols)
                for key in visitedEmployees:
                    if not visitedEmployees[key][0]:
                        flag = 0
                        break
                    newSum += visitedEmployees[key][1]
                if flag and newSum < min_sum:
                    min_sum = newSum
                    location = [i, j]
                reDefineVisitedEmployees()
                reDefineVisitedSpaces(rows, cols)
    return location

# make matrix map from file
def make_map(file):
    map_ = []
    with open(file, 'r') as my_file:
        lines = my_file.readlines()
        for line in lines:
            if line[-1] == '\n':
                map_.append(list(line)[:-1])
            else:
                map_.append(list(line))
    rows = len(map_)
    cols = len(map_[0])
    return map_, rows, cols

# main program
if __name__ == '__main__':
    map_, rows, cols = make_map('map.txt')
    print("\n               * map *\n")
    for row in map_:
        print(row)
    print()
    print(f"best kitchen location: {find_path(map_, rows, cols)}")

