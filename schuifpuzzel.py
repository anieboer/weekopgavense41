import math
import heapq

class PriorityQueue:
    # to be use in the A* algorithm
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    # in a min-heap, the keys of parent nodes are less than or equal to those
    # of the children and the lowest key is in the root node
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]


# maak het doel
def generate_goal_field(n):
    # TODO generate goal field based on n
    goal_field = [[]] * 3
    goal_field[0] = [1, 2, 3]
    goal_field[1] = [4, 5, 6]
    goal_field[2] = [7, 8, 0]
    return goal_field


# maak een veld
def generate_field(n):
    # TODO generate field nxn
    field = [[]] * 3
    field[0] = [1, 8, 2]
    field[1] = [0, 4, 3]
    field[2] = [7, 6, 5]
    return field


def get_grid_values(coordinate):
    row = coordinate[0]
    col = coordinate[1]
    field_value = field[row][col]
    goal_value = goal_field[row][col]
    return field_value, goal_value


def distance_between(start, goal):
    # TODO
    # isn't distance between neighbours always 1?
    return 1


def heuristic_cost_estimate(start, goal):
    # TODO make guess
    # assuming any tile can swap with any tile it would only take the number of
    # horizontal steps added to the number of vertical steps
    # vertical = goal[0] - start[0]
    # horizontal = goal[1] - start[1]
    # guess = horizontal + vertical
    guess = n+n
    return guess


def find_value(value):
    coord_goal = ()
    coord_field = ()
    for i, x in enumerate(goal_field):
        try:
            coord_goal = (i, x.index(value))
        except ValueError:
            pass
    for i, x in enumerate(field):
        try:
            coord_field = (i, x.index(value))
        except ValueError:
            pass
    return coord_field, coord_goal


def neighbours(coordinate):
    row = coordinate[0]
    col = coordinate[1]

    left = ((row - 1), col)
    if left < (0, col):
        left = None
    right = ((row + 1), col)
    if right > ((n - 1), col):
        right = None
    up = (row, (col - 1))
    if up < (row, 0):
        up = None
    down = (row, (col + 1))
    if down > (row, (n -1)):
        down = None

    return left, right, up, down


def backtrack(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return list(reversed(total_path))


def a_ster(start, goal):
    closedSet = set()
    frontier = PriorityQueue()
    came_from = {}
    g_score = {}
    f_score = {}
    g_score[start] = 0
    f_score[start] = heuristic_cost_estimate(start, goal)
    frontier.put(start, 0.0)
    closedSet.add(start)

    while not frontier.empty():
        # do something
        current = frontier.get()
        if current == goal:
            print("Goal reached yay")
            print("goal: " + str(goal) + " value: " + str(get_grid_values(goal)[1]))
            return print(backtrack(came_from, current))

        if current in came_from:
            continue

        closedSet.add(current)
        for neighbour in neighbours(current):
            # do something
            if neighbour is not None:
                if neighbour not in closedSet:
                    tentative_gscore = g_score.setdefault(current, math.inf) + distance_between(current, neighbour)

                    if neighbour not in g_score.keys():
                        g_score[neighbour] = tentative_gscore
                    elif tentative_gscore >= g_score[neighbour]:
                        continue

                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_gscore
                    f_score[neighbour] = g_score[neighbour] + heuristic_cost_estimate(neighbour, goal)

                    frontier.put(neighbour, f_score[neighbour])



def main():
    # goal_field = generate_goal_field(n)
    # field = generate_field(n)
    print("goal: " + str(goal_field))
    print("field: " + str(field))
    all_coordinates = [(x,y) for x in range(n) for y in range(n)]
    for coordinate in all_coordinates:
        field_value, goal_value = get_grid_values(coordinate)
        # print(field_value)
        # print(goal_value)
        # print("from find_value:")
        found_coord1, found_coord2 = find_value(field_value)
        # print(found_coord1)
        # print(found_coord2)
        a_ster(found_coord1, found_coord2)



# kies een N
n = 3
goal_field = generate_goal_field(n)
field = generate_field(n)

if __name__ == '__main__':
    main()
