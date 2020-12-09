from util import Node, StackFrontier, QueueFrontier
from copy import deepcopy

# get input
k, m, n = map(int, input().split())
packs = []
for _ in range(k):
    packs.append(input().split())
print(packs)

def sort_and_categorize_by_color(source):
    start = Node(state=source, parent=None, action=None)
    queueFrontier = QueueFrontier()
    queueFrontier.add(start)

    explored = set()
    num_explored = 0

    while True:
        if queueFrontier.empty():
            return None
        node = queueFrontier.remove()
        # print("id= {}".format(node.state))
        num_explored += 1

        if node.is_goal():
            cells = []
            while node.parent is not None:
                cells.append([node.action, node.state])
                node = node.parent
            cells.reverse()
            return cells
        explored.add(node.state)

        # Add neighbors
        neighbors = list(neighbors_for_packs(node.state))
        for neighbor in neighbors:
            neighbor = list(neighbor)
            if not queueFrontier.contains_state(neighbor[1]) and neighbor[1] not in explored:
                child = Node(state=neighbor[1], parent=node, action=neighbor[0])
                queueFrontier.add(child)

def neighbors_for_packs(state):
    neighbors = list()
    for i in range(len(state) - 1):
        for j in range(i+1,len(state) - 1):
            origin, destination = None
            mark = 0
            if state[i][0][:-1] < state[j][0][:-1]:
                origin = i
                destination = j
                mark = 1
            elif state[i][0][:-1] > state[j][0][:-1]:
                origin = j
                destination = i
                mark = 1

            if mark == 1:
                temp_packs = deepcopy(state)
                card = temp_packs[origin].pop(0)
                temp_packs[destination].insert(0, card)
                neighbors.append(temp_packs)

