import matplotlib.pyplot as plt
import numpy as np


def visualize_tour(points, tour):
    '''Функция для визуализации полученного маршрута'''
    x_coords, y_coords = zip(*points)

    # Добавление первой точки в конец тура для замыкания цикла
    tour.append(tour[0])

    tour_x = [x_coords[i] for i in tour]
    tour_y = [y_coords[i] for i in tour]

    plt.figure(figsize=(8, 6))
    plt.plot(x_coords, y_coords, 'o', markersize=10, label='Точки')
    plt.plot(tour_x, tour_y, 'r-', linewidth=2, label='Гамильтонов цикл')

    for i, (x, y) in enumerate(points):
        plt.text(x, y, f'  {i}', fontsize=16, ha='right', va='center')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.axis('equal')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Ввод из файла
def read_pairs_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    N = int(lines[0].strip())

    # Читаем N пар чисел
    pairs = []
    for line in lines[1:N + 1]:
        a, b = map(int, line.split())
        pairs.append((a, b))

    return pairs


coords = read_pairs_from_file("tsp_problem.txt")

print(distance(coords))


def distance(coords):
    n = len(coords)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            matrix[i][j] = np.sqrt((coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2)
            matrix[j][i] = matrix[i][j]
    return matrix

# Nearest neighbour

def solver_nn(coords):
    n = len(coords)
    dist = 0
    matrix = distance(coords)
    tour = []
    tour.append(0)
    node = 0
    matrix[0][0] = 10 ** 11
    for i in range(n):
        matrix[0][i] = 10**11
    for i in range(n - 1):
        min = 10 ** 10
        min_index = None
        for j in range(n):
            if (matrix[j][node] < min):
                min_index = j
                min = matrix[j][node]
        for k in range(n):
            matrix[node][k] = 10**11
        matrix[min_index][min_index] = 10 ** 11
        node = min_index
        tour.append(node)
        dist += min
    dist += matrix[node][0]
    return dist, tour
dist, tour = solver_nn(coords)
print(dist)
print(tour)
visualize_tour(coords, tour)