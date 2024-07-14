import random


def greedy_max_cut(num_nodes, edges):
    A = set()
    B = set()
    start_node = random.randint(0, num_nodes - 1)
    A.add(start_node)

    remaining_nodes = set(range(num_nodes))
    remaining_nodes.remove(start_node)

    half = num_nodes // 2

    while remaining_nodes:
        if len(A) == half:
            B.update(remaining_nodes)
            break
        elif len(B) == half:
            A.update(remaining_nodes)
            break

        max_gain = float('-inf')
        best_node = None
        best_set = None

        for node in remaining_nodes:
            gain_A = 0
            gain_B = 0

            for edge in edges:
                if edge[0] == node:
                    if edge[1] in A:
                        gain_B += edge[2]
                    elif edge[1] in B:
                        gain_A += edge[2]
                elif edge[1] == node:
                    if edge[0] in A:
                        gain_B += edge[2]
                    elif edge[0] in B:
                        gain_A += edge[2]

            if len(A) < half and gain_A > max_gain:
                max_gain = gain_A
                best_node = node
                best_set = A
            if len(B) < half and gain_B > max_gain:
                max_gain = gain_B
                best_node = node
                best_set = B

        best_set.add(best_node)
        remaining_nodes.remove(best_node)

    cut_weight = 0
    for edge in edges:
        if (edge[0] in A and edge[1] in B) or (edge[0] in B and edge[1] in A):
            cut_weight += edge[2]

    return A, B, cut_weight


# Пример использования
num_nodes = 6
edges = [
    (0, 1, 1),
    (0, 2, 2),
    (1, 2, 3),
    (1, 3, 4),
    (2, 3, 5),
    (3, 4, 6),
    (4, 5, 7)
]
A, B, cut_weight = greedy_max_cut(num_nodes, edges)
print("Set A:", A)
print("Set B:", B)
print("Cut weight:", cut_weight)


def read_edges_from_file(file_path):
    edges = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) != 3:
                continue
            i, j, w = map(int, parts)
            edges.append((i, j, w))
    return n, edges

num_nodes, edges = read_edges_from_file("maxcut.txt")
A, B, cut_weight = greedy_max_cut(num_nodes, edges)
print("Set A:", A)
print("Set B:", B)
print("Cut weight:", cut_weight)
