import tkinter as tk
from tkinter import ttk

import random
import threading
import heapq
import math

# assuming a resulution of 1920 x 1080 = 16 : 9

# global color scheme
bgc = '#FDF6E3'
gridc = '#542437'
blockc = 'red'
pathc = 'blue'
startc = '#C7F464'
goalc = 'yellow'

# global vars
PAUSE_STATUS = False
PROB = 0.1  # probability blocking node
SIZE = 25  # the nr of nodes=grid crossings in a row (or column)

# global var: pixel sizes
CELL = 35  # size of cell/square in pixels
W = (SIZE - 1) * CELL  # width of grid in pixels
H = W  # height of grid
TR = 10  # translate/move the grid, upper left is 10,10

grid = [[0 for x in range(SIZE)] for y in range(SIZE)]
start = (0, 0)
goal = (SIZE - 1, SIZE - 1)


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


def neighbours(node: tuple):
    """Find the neighbours for the given node"""
    row = node[0]
    col = node[1]

    left = (row - 1, col)
    if left < (0, col):
        left = None
    right = (row + 1, col)
    if right > (SIZE - 1, col):
        right = None
    up = (row, col - 1)
    if up < (row, 0):
        up = None
    down = (row, col + 1)
    if down > (row, SIZE - 1):
        down = None

    return left, right, up, down


def backtrack(doel, parents):
    pad = []
    while doel:
        pad.append(doel)
        doel = parents[doel]
    return list(reversed(pad))


def backtrack_aster(parents: dict, current):
    total_path = [current]
    while current in parents.keys():
        current = parents[current]
        total_path.append(current)
    return list(reversed(total_path))


def draw(path):
    buf = path
    if len(buf) > 2:
        plot_line_segment(canvas, buf[0][0], buf[0][1], buf[1][0], buf[1][1])
        del buf[0]
        canvas.update_idletasks()
        draw(buf)
    plot_line_segment(canvas, buf[0][0], buf[0][1], SIZE - 1, SIZE - 1)


def heuristic_cost_estimate(node: tuple, goal: tuple) -> int:
    x = goal[0] - node[0]
    y = goal[1] - node[1]
    guess = math.sqrt((x*x) + (y*y))
    return guess


def Aster():
    visited = set()
    frontier = PriorityQueue()
    came_from = {}
    g_score = {}

    g_score[start] = 0

    f_score = {}
    f_score[start] = heuristic_cost_estimate(start, goal)

    frontier.put(start, priority=0.0)

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            print("Reached goal with A*!")
            print("Route is: ")
            print(backtrack_aster(came_from, current))
            draw(backtrack_aster(came_from, current))

        if current in visited:
            continue

        visited.add(current)

        for neighbour in neighbours(current):
            if neighbour is not None:
                if neighbour not in visited:
                    if get_grid_value(neighbour) is not 'b':
                        tentative_gscore = grid_cost[current] + grid_cost[neighbour]

                        if neighbour not in g_score.keys():
                            g_score[neighbour] = tentative_gscore
                        elif tentative_gscore >= g_score[neighbour]:
                            continue

                        came_from[neighbour] = current
                        g_score[neighbour] = tentative_gscore
                        f_score[neighbour] = g_score[neighbour] + heuristic_cost_estimate(neighbour, goal)

                        frontier.put(neighbour, f_score[neighbour])

                    else:
                        # no need to visit if blocked
                        visited.add(neighbour)


def UCS():
    frontier = PriorityQueue()
    visited = set()
    distance = {}
    parents = {}

    frontier.put(start, priority=0.0)
    distance[start] = 0
    parents[start] = None

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            print("Reached goal using UCS!")
            print("Route is: ")
            print(backtrack(goal, parents))
            draw(backtrack(goal, parents))
            continue

        if current in visited:
            continue

        visited.add(current)

        for neighbour in neighbours(current):
            if neighbour is not None:
                if neighbour not in visited:
                    if get_grid_value(neighbour) is not 'b':
                        # priority = s.priority + cost(s, neighbor)
                        local_cost = grid_cost[current] + grid_cost[neighbour]
                        if neighbour not in distance.keys() or distance[neighbour] > local_cost:
                            distance[neighbour] = local_cost
                            parents[neighbour] = current
                            frontier.put(neighbour, local_cost)
                    else:
                        # if a neighbour is blocked, no need to visit
                        visited.add(neighbour)


def bernoulli_trial():
    return 1 if random.random() < PROB else 0


def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]


def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value


def make_grid(c):
    # vertical lines
    for i in range(0, W + 1, CELL):
        c.create_line(i + TR, 0 + TR, i + TR, H + TR, fill=gridc)

    # horizontal lines
    for i in range(0, H + 1, CELL):
        c.create_line(0 + TR, i + TR, W + TR, i + TR, fill=gridc)


def init_grid(c):
    for x in range(SIZE):
        for y in range(SIZE):
            node = (x, y)
            # start and goal cannot be bloking nodes
            if bernoulli_trial() and node != start and node != goal:
                set_grid_value(node, 'b')  # blocked
                plot_node(c, node, color=blockc)
            else:
                set_grid_value(node, -1)  # init costs, -1 means infinite


def plot_line_segment(c, x0, y0, x1, y1):
    c.create_line(x0 * CELL + TR, y0 * CELL + TR, x1 * CELL + TR, y1 * CELL + TR, fill=pathc, width=2)


def plot_node(c, node, color):
    # size of (red) rectangle is 8 by 8
    x0 = node[0] * CELL - 4
    y0 = node[1] * CELL - 4
    x1 = x0 + 8 + 1
    y1 = y0 + 8 + 1
    c.create_rectangle(x0 + TR, y0 + TR, x1 + TR, y1 + TR, fill=color)


def control_panel():
    mf = ttk.LabelFrame(right_frame)
    mf.grid(column=0, row=0, padx=8, pady=4)
    mf.grid_rowconfigure(2, minsize=10)

    def start():
        target = bt_alg.get()
        if target == 'UC':
            t = threading.Thread(target=UCS())
        else:
            t = threading.Thread(target=Aster())
        t.start()
        if not t.isAlive():
            print()
            print("Finished " + target)

    def pause():
        global PAUSE_STATUS
        if PAUSE_STATUS:
            pause_button.configure(background='SystemButtonFace')
            PAUSE_STATUS = False
        else:
            pause_button.configure(background='red')
            PAUSE_STATUS = True

    start_button = tk.Button(mf, text="Start", command=start, width=10)
    start_button.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    pause_button = tk.Button(mf, text="Pause", command=pause, width=10)
    pause_button.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    def sel():
        print('algorithm =', bt_alg.get())

    r1_button = tk.Radiobutton(mf, text='UC', value='UC', variable=bt_alg, command=sel)
    r2_button = tk.Radiobutton(mf, text='A*', value='A*', variable=bt_alg, command=sel)
    bt_alg.set('UC')

    r1_button.grid(row=3, column=1, columnspan=2, sticky='w')
    r2_button.grid(row=4, column=1, columnspan=2, sticky='w')

    def box_update1(event):
        print('speed is set to:', box1.get())

    def box_update2(event):
        global PROB
        PROB = (int(box2.get()) / 10)
        print('prob. blocking is set to:', box2.get())
        # genereer opnieuw een veld
        make_grid(canvas)
        init_grid(canvas)
        # block nodes blijven hangen?

    lf = ttk.LabelFrame(right_frame, relief="sunken")
    lf.grid(column=0, row=1, padx=5, pady=5)

    ttk.Label(lf, text="Speed ").grid(row=1, column=1, sticky='w')
    box1 = ttk.Combobox(lf, textvariable=speed, state='readonly', width=6)
    box1.grid(row=2, column=1, sticky='w')
    box1['values'] = tuple(str(i) for i in range(10))
    box1.current(5)
    box1.bind("<<ComboboxSelected>>", box_update1)

    ttk.Label(lf, text="Prob. blocking").grid(row=3, column=1, sticky='w')
    box2 = ttk.Combobox(lf, textvariable=prob, state='readonly', width=6)
    box2.grid(row=4, column=1, sticky='ew')
    box2['values'] = tuple(str(i) for i in range(10))
    box2.current(1)
    box2.bind("<<ComboboxSelected>>", box_update2)


root = tk.Tk()
root.title('A* demo')

speed = tk.StringVar()
prob = tk.StringVar()
bt_alg = tk.StringVar()
left_frame = ttk.Frame(root, padding="3 3 12 12")
left_frame.grid(column=0, row=0)

right_frame = ttk.Frame(root, padding="3 3 12 12")
right_frame.grid(column=1, row=0)

canvas = tk.Canvas(left_frame, height=H + 4 * TR, width=W + 4 * TR, borderwidth=-TR, bg=bgc)
canvas.pack(fill=tk.BOTH, expand=True)

make_grid(canvas)
init_grid(canvas)

# plot a sample path for demonstration
# for i in range(SIZE - 1):
#     plot_line_segment(canvas, i, i, i, i + 1)
#     plot_line_segment(canvas, i, i + 1, i + 1, i + 1)

# show start and goal nodes
plot_node(canvas, start, color=startc)
plot_node(canvas, goal, color=goalc)

# give grid cost
# for height in range(len(grid)):
#     for width in range(len(grid[0])):
#         if get_grid_value(width, height) is not 'b':
#             set_grid_value((width, height), random.randint(1, 9))

grid_cost = {}
for height in range(len(grid)):
    for width in range(len(grid[0])):
        if get_grid_value((width, height)) is not 'b':
            # grid_cost[(width, height)] = random.randint(1, 9)
            grid_cost[(width, height)] = 1

if __name__ == "__main__":
    control_panel()
    root.mainloop()
