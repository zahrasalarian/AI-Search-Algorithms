from util import Node, StackFrontier, QueueFrontier
from copy import deepcopy

produced_num = 0
explored_num = 0
def main():
    # get input
    k, m, n = map(int, input().split())
    packs = list()
    for _ in range(k):
        pack = input().split()
        if pack == ['#']:
            packs.append([])
            continue
        else:
            pack.reverse()
            packs.append(pack)
    print(packs)

    path = sort_and_categorize_by_color(packs)
    if path is None:
        print("Not found.")
    else:
        print(path)
    print("produced nodes = {}".format(produced_num))
    print("explored nodes = {}".format(explored_num))

def sort_and_categorize_by_color(source):
    global produced_num
    global explored_num
    start = Node(state=source, parent=None, depth=0)
    queueFrontier = QueueFrontier()
    queueFrontier.add(start)

    explored = list()

    while True:
        if queueFrontier.empty():
            return None
        node = queueFrontier.remove()
        explored_num += 1

        if node.is_goal():
            print("goal depth = {}".format(node.depth))
            cells = []
            while node.parent is not None:
                state = node.state
                for pack in state:
                    pack.reverse()
                cells.append(state)
                node = node.parent
            for pack in source:
                pack.reverse()
            cells.append(source)
            cells.reverse()
            return cells
        explored.append(node.state)

        # Add neighbors
        neighbors = list(neighbors_for_packs(node.state))
        produced_num += len(neighbors)
        for neighbor in neighbors:
            neighbor = list(neighbor)
            if not queueFrontier.contains_state(neighbor) and neighbor not in explored:
                child = Node(state=neighbor, parent=node, depth=node.depth+1)
                queueFrontier.add(child)

def neighbors_for_packs(state):
    neighbors = list()
    for i in range(len(state) - 1):
        for j in range(i+1, len(state)):
            origin = None
            destination = None
            mark = 0
            if len(state[i]) == 0 and len(state[j]) != 0:
                origin = j
                destination = i
                mark = 1
            elif len(state[j]) == 0 and len(state[i]) != 0:
                origin = i
                destination = j
                mark = 1
            elif len(state[j]) == 0 and len(state[i]) == 0:
                continue
            elif state[i][0][:-1] < state[j][0][:-1]:
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
    return neighbors

if __name__ == "__main__":
    main()