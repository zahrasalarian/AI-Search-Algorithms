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
    # print(packs)

    path = sort_and_categorize_by_color(packs)
    if path is None:
        print("Not found.")
    else:
        # degrees = len(path)
        # print(f"{degrees} degrees of separation.")
        # path = [(None, source)] + path
        # for i in range(degrees):
        #     person1 = people[path[i][1]]["name"]
        #     person2 = people[path[i + 1][1]]["name"]
        #     movie = movies[path[i + 1][0]]["title"]
        #     print(f"{i + 1}: {person1} and {person2} starred in {movie}")
        print(path)

def sort_and_categorize_by_color(source):
    start = Node(state=source, parent=None)
    queueFrontier = QueueFrontier()
    queueFrontier.add(start)

    explored = list()
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
                cells.append([node.state])
                node = node.parent
            cells.reverse()
            return cells
        explored.append(node.state)

        # Add neighbors
        neighbors = list(neighbors_for_packs(node.state))
        for neighbor in neighbors:
            neighbor = list(neighbor)
            if not queueFrontier.contains_state(neighbor) and neighbor not in explored:
                child = Node(state=neighbor, parent=node)
                queueFrontier.add(child)

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