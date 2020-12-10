from util import Node, StackFrontier, QueueFrontier
from copy import deepcopy

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
    print(packs)

    path = ids(packs,limit)
    if path is None:
        print("Not found.")
    else:
        print(path)

def ids(source,limit):
    for i in range(limit,limit + 50):
        print(i)
        path = sort_and_categorize_by_color(source,i)
        if path is not None:
            return path
        else:
            continue

def sort_and_categorize_by_color(source,limit):
    start = Node(state=source, parent=None,depth=0)
    stackFrontier = StackFrontier()
    stackFrontier.add(start)

    explored = list()
    num_explored = 0

    counter = 0
    while True:
        if stackFrontier.empty():
            return None
        node = stackFrontier.remove()
        num_explored += 1

        if node.is_goal():
            cells = []
            while node.parent is not None:
                cells.append(node.state)
                node = node.parent
            cells.reverse()
            return cells
        explored.append(node.state)

        # Add neighbors if we haven't reached the limit
        if node.depth < limit:
            neighbors = list(neighbors_for_packs(node.state))
            for neighbor in neighbors:
                neighbor = list(neighbor)
                # neighbor = sorted(neighbor, key=lambda x: x[1], reverse=True)
                if not stackFrontier.contains_state(neighbor) and neighbor not in explored:
                    child = Node(state=neighbor, parent=node, depth=node.depth+1)
                    stackFrontier.add(child)
            counter += 1

def neighbors_for_packs(state):
    neighbors = list()
    # print(state)
    for i in range(len(state) - 1):
        for j in range(i+1,len(state)):
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
                # print(temp_packs)
                neighbors.append(temp_packs)
    # print("*********")
    return neighbors

if __name__ == "__main__":
    main()