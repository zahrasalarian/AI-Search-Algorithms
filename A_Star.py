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
    # will be completed later
    return node.depth + 2

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
                cells.append(node.state)
                node = node.parent
            cells.reverse()
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
                new_g = node.G + node.move_cost(neighbor)
                if neighbor.G > new_g:
                    # If so, update the node to have a new parent
                    neighbor.G = new_g
                    neighbor.parent = node
            else:
                # If it isn't in the open set, calculate the G and H score for the node
                neighbor.G = node.g + 1
                neighbor.H = heuristic(neighbor)
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