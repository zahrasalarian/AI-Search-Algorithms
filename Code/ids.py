from util import Node, StackFrontier, QueueFrontier
from copy import deepcopy

produced_num = 0
explored_num = 0

def main():
    # get input
    k, m, n = map(int, input().split())
    limit = int(input())
    packs = list()
    for _ in range(k):
        pack = input().split()
        if pack == ['#']:
            packs.append([])
            continue
        else:
            pack.reverse()
            packs.append(pack)

    path = ids(packs, limit)
    if path is None:
        print("Not found.")
    else:
        print(path)
    print("produced nodes = {}".format(produced_num))
    print("explored nodes = {}".format(explored_num))

def ids(source,limit):
    node = Node(state=source, parent=None, depth=0)
    for i in range(limit, limit + 50):
        # print(i)
        path = sort_and_categorize_by_color(node, i)
        if path is not None:
            path.insert(0, source)
            return path
        else:
            continue
    return None

def sort_and_categorize_by_color(source, limit):
    global explored_num
    global produced_num
    node = source

    explored = list()
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
        for pack in node.state:
            pack.reverse()
        cells.reverse()
        return cells
    explored.append(node.state)

    if limit <= 0:
        return None
    neighbors = list(neighbors_for_packs(node.state))
    produced_num += len(neighbors)


    for i in range(len(neighbors)):
        child = Node(state=neighbors[i], parent=node, depth=node.depth+1)
        result = sort_and_categorize_by_color(child, limit - 1)
        if result is not None:
            return result

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