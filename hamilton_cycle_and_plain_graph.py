import copy
import sys


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# For a graph, we calculate the neighbors of every point
# alphabet, every point has a character of the alphabet as id
# Returns a list that for every point in graph has another list
# that represents the neighbors of point
def neighbors(graph):
    neighbors_table = []
    for index, line in enumerate(graph):
        neighbors_list = []
        alphabet_pos = 0
        for ch in line:
            if(ch == "1" and index != alphabet_pos):
                neighbors_list.append(alphabet[alphabet_pos])
            if(ch != " "):
                alphabet_pos += 1
        neighbors_table.append(neighbors_list)

    return neighbors_table


# Returns a list that for every point in graph has another list
# that holds vertices of the point
def vertices(M):
    table = copy.deepcopy(M)
    for index, neighbors_list in enumerate(table):
        for index2, ch in enumerate(neighbors_list):
            table[index][index2] = alphabet[index] + ch

    return table


# creates a set so you can start working on checking if
# the graph is plain
def create_set(hamiltonian_cycle, updated_neighbors_table):
    vertices_set = []
    done = True
    pos_hamilton = 0

    # the first check at while is in case that no one has a second neighbor
    # if the first node has no extra neighbors then go to the next node
    # until you find a node with neighbors or reach the end of hamilton ccycleircle
    while (pos_hamilton < len(hamiltonian_cycle) and done):
        ch_in_ham = hamiltonian_cycle[pos_hamilton]
        pos_in_alphabet = alphabet.find(ch_in_ham)
        if (len(updated_neighbors_table[pos_in_alphabet]) > 0):
            done = False

            # Create set of vertices
            for ch in updated_neighbors_table[pos_in_alphabet]:
                vertices_set.append(ch_in_ham + ch)
                updated_neighbors_table[alphabet.find(ch)].remove(ch_in_ham)

        else:
            pos_hamilton += 1

    return (done, vertices_set, pos_hamilton)


def should_go(path, at_set, i, j):
    for a in at_set:
        # check 00,
        # if one side of vertice is inside from j to i path
        # check 01 and 02
        # if the other side of vertice has anything to do with
        # the path
        check00 = (path.find(a[0]) >= 0)
        check01 = (a[1] == alphabet[i])
        check02 = (a[1] == j)

        # checks10, 11 12 do the same as 00, 01, 02 for the other side
        check10 = (path.find(a[1]) >= 0)
        check11 = (a[0] == alphabet[i])
        check12 = (a[0] == j)
        if ((check00) and not (check01 or check02)
                or (check10) and not (check11 or check12)):
            return False

    return True


def main():
    graph = open("graph.txt", "r")
    neighbors_table = neighbors(graph)
    path_table = vertices(neighbors_table)

    repeats = 0
    while (repeats < len(path_table) - 2):
        graph_path = []
        for vertices_list in path_table:
            temp_path = []
            for path in vertices_list:
                for ch in neighbors_table[alphabet.find(path[len(path) - 1])]:
                    if(path.find(ch) < 0):
                        temp_path.append(path + ch)
            graph_path.append(temp_path)

        path_table = copy.deepcopy(graph_path)
        repeats += 1

    # check if you can have a cycle
    for vertices_list in path_table:
        cycle = []
        for path in vertices_list:
            for ch in neighbors_table[alphabet.find(path[len(path) - 1])]:
                if(path[0] == ch):
                    cycle.append(path + ch)

    if (len(cycle) == 0):
        print("No Hamiltonian cycle. Exit program")
        sys.exit()

    hamiltonian_cycle = cycle[0]
    print("A Hamiltonian cycle is:")
    print(hamiltonian_cycle)

    # start the proccess to find if the graph is a plain
    updated_neighbors_table = copy.deepcopy(neighbors_table)

    # remove the paths from hamiltonian cycle
    for i, j in zip(hamiltonian_cycle[:len(hamiltonian_cycle) - 1],
                    hamiltonian_cycle[1:]):
        try:
            updated_neighbors_table[alphabet.find(i)].remove(j)
            updated_neighbors_table[alphabet.find(j)].remove(i)
        except ValueError:
            print("There was an error")
            print("The graph should be undirected")
            print("Exiting")
            sys.exit()

    # Creates group A and B
    A = []
    B = []

    a_done, A, pos_hamilton = create_set(
        hamiltonian_cycle,
        updated_neighbors_table)

    if (a_done):
        print("There is no possible path for creating group A." +
              "The graph is a level graph")
        sys.exit()

    # remove the vertices from neighbors_table
    updated_neighbors_table[
        alphabet.find(hamiltonian_cycle[pos_hamilton])] = []

    b_done, B, pos_hamilton = create_set(
        hamiltonian_cycle,
        updated_neighbors_table)

    if (b_done):
        print("There is no possible path for creating the group B." +
              "This is a level graph ")
        sys.exit()

    # remove the vertices from neighbors_table
    updated_neighbors_table[alphabet.find(
        hamiltonian_cycle[pos_hamilton])] = []

    i = 0
    while i < len(updated_neighbors_table):
        if (len(updated_neighbors_table[i]) > 0):
            for j in updated_neighbors_table[i]:
                # find the path between j and one of his neighbors
                # at hamiltonian path
                a = hamiltonian_cycle.find(alphabet[i])
                b = hamiltonian_cycle.find(j)
                if a < b:
                    j_to_i = hamiltonian_cycle[a + 1: b]
                else:
                    j_to_i = hamiltonian_cycle[b + 1: a]

                # try to put j_to_i at A
                a_done = True
                b_done = True

                a_done = should_go(j_to_i, A, i, j)
                if (a_done):
                    A.append(alphabet[i] + j)
                    updated_neighbors_table[alphabet.find(j)].remove(
                        alphabet[i])
                else:
                    b_done = should_go(j_to_i, B, i, j)
                    if(b_done):
                        B.append(alphabet[i] + j)
                        updated_neighbors_table[alphabet.find(j)].remove(
                            alphabet[i])

                if(not a_done and not b_done):
                    print("This is not level graph ")
                    sys.exit()
        i += 1

    print("This is a level graph, the two groups of edges are: ")
    print(A)
    print(B)


if (__name__ == "__main__"):
    main()  # ABCDEFGHI
