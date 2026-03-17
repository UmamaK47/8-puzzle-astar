import heapq

goal_state = ((1,2,3),
              (4,5,6),
              (7,8,0))

moves = [(-1,0),(1,0),(0,-1),(0,1)]

class Node:

    def __init__(self,state,parent=None,move=None,g=0):

        self.state = state
        self.parent = parent
        self.move = move
        self.g = g
        self.h = self.heuristic()
        self.f = self.g + self.h

    def heuristic(self):

        distance = 0

        for i in range(3):
            for j in range(3):

                value = self.state[i][j]

                if value != 0:

                    goal_x = (value-1)//3
                    goal_y = (value-1)%3

                    distance += abs(goal_x-i) + abs(goal_y-j)

        return distance

    def __lt__(self,other):

        return self.f < other.f


def find_blank(state):

    for i in range(3):
        for j in range(3):

            if state[i][j]==0:
                return i,j


def generate_successors(node):

    successors=[]

    x,y = find_blank(node.state)

    for dx,dy in moves:

        nx = x+dx
        ny = y+dy

        if 0<=nx<3 and 0<=ny<3:

            new_state = [list(row) for row in node.state]

            new_state[x][y],new_state[nx][ny] = new_state[nx][ny],new_state[x][y]

            new_state = tuple(tuple(row) for row in new_state)

            successors.append(
                Node(new_state,node,(nx,ny),node.g+1)
            )

    return successors


def reconstruct_path(node):

    path=[]

    while node:

        path.append(node.state)
        node=node.parent

    return path[::-1]


def astar(start):

    open_list=[]
    closed=set()

    start_node = Node(start)

    heapq.heappush(open_list,start_node)

    while open_list:

        current = heapq.heappop(open_list)

        if current.state == goal_state:

            return reconstruct_path(current)

        closed.add(current.state)

        successors = generate_successors(current)

        for child in successors:

            if child.state in closed:
                continue

            heapq.heappush(open_list,child)

    return None


def print_state(state):

    for row in state:
        print(row)
    print()


start_state=((1,2,3),
             (4,0,6),
             (7,5,8))


solution = astar(start_state)

if solution:

    print("Solution Path:\n")

    for step,state in enumerate(solution):

        print("Move:",step)
        print_state(state)

    print("Total Moves:",len(solution)-1)

else:

    print("No solution found")