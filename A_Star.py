from util import Node, StackFrontier, QueueFrontier
from copy import deepcopy

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

    path = aStar(packs)
    if path is None:
        print("Not found.")
    else:
        print(path)

def heuristic(node):
    state = node.state
    conf_num = 0
    for pack in state:
        if len(pack) == 0:
            continue
        main_color = pack[-1][-1:]
        prev_value = int(pack[-1][:-1])
        for i in range(len(pack)-1, -1, -1):
            # color or value
            color = pack[i][-1:]
            if (color != main_color) or (int(prev_value) < int(pack[i][:-1])):
                conf_num += i + 1
                break
            else:
                prev_value = int(pack[i][:-1])
    return conf_num
def aStar(source):
    # The open and closed sets
    openset = set()
    closedset = set()
    # Current point is the starting point
    start = Node(state=source, parent=None, depth=0)
    # Add the starting point to the open set
    openset.add(start)
    # While the open set is not empty
    while openset:
        # Find the item in the open set with the lowest G + H score
        node = min(openset, key=lambda o: o.g + o.h)
        # If it is the item we want, retrace the path and return it
        if node.is_goal():
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
            # if len(cells) == 0:
            #     cells.append(node.state)
            return cells
        # Remove the item from the open set
        openset.remove(node)
        # Add it to the closed set
        closedset.add(node)
        # Loop through the node's children/siblings
        neighbors = list(neighbors_for_packs(node.state))
        for neighbor_state in neighbors:
            neighbor = Node(state=neighbor_state, parent=node, depth=node.depth + 1)
            # If it is already in the closed set, skip it
            if neighbor in closedset:
                continue
            # Otherwise if it is already in the open set
            if neighbor in openset:
                # Check if we beat the G score
                new_g = node.g + 1
                if neighbor.g > new_g:
                    # If so, update the node to have a new parent
                    neighbor.g = new_g
                    neighbor.parent = node
            else:
                # If it isn't in the open set, calculate the G and H score for the node
                neighbor.g = node.g + 1
                neighbor.h = heuristic(neighbor)
                # print(neighbor.state)
                # print(neighbor.h)
                # print("*********")
                # Set the parent to our current item
                neighbor.parent = node
                # Add it to the set
                openset.add(neighbor)
    # return None if there is no path
    return None


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
            else:
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