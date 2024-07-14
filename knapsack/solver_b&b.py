import heapq

'''
Создадим класс, объекты которого будут хранить информацию о том, какую на данный момент мы получили прибыль
и какую часть рюкзака какими объектами заняли, а также какую потенциальную прибыль мы можем получить
'''


class Node:
    def __init__(self, level, profit, weight, bound, included_items):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.bound = bound
        self.included_items = included_items

    def __lt__(self, other):
        return self.bound > other.bound


'''
Данная функция вычисляет потенциальную прибыль
'''


def bound(node, n, W, items):
    if node.weight >= W:
        return 0
    profit_bound = node.profit
    j = node.level + 1
    totweight = node.weight

    while j < n and totweight + items[j][1] <= W:
        totweight += items[j][1]
        profit_bound += items[j][0]
        j += 1

    if j < n:
        profit_bound += (W - totweight) * items[j][0] / items[j][1]

    return profit_bound


def knapsack(items, W):
    n = len(items)
    items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    Q = []
    u = Node(-1, 0, 0, 0, [])
    v = Node(-1, 0, 0, 0, [])
    u.bound = bound(u, n, W, items)
    maxProfit = 0
    maxItems = []

    heapq.heappush(Q, u)

    while Q:
        # Пока не перебрали все возможные варианты, извлекаем узел из кучи
        u = heapq.heappop(Q)
        if u.bound > maxProfit:
            v.level = u.level + 1

            # С учётом взятого на данном уровне предмета и без него


            v.weight = u.weight + items[v.level][1]
            v.profit = u.profit + items[v.level][0]
            v.included_items = u.included_items + [v.level]

            if v.weight <= W and v.profit > maxProfit:
                maxProfit = v.profit
                maxItems = v.included_items

            v.bound = bound(v, n, W, items)
            if v.bound > maxProfit:
                heapq.heappush(Q, Node(v.level, v.profit, v.weight, v.bound, v.included_items))

            v.weight = u.weight
            v.profit = u.profit
            v.included_items = u.included_items
            v.bound = bound(v, n, W, items)
            if v.bound > maxProfit:
                heapq.heappush(Q, Node(v.level, v.profit, v.weight, v.bound, v.included_items))

    selected_items = [(items[i][0], items[i][1]) for i in maxItems]
    return maxProfit, selected_items


def read_input_from_file(filename):
    with open(filename, 'r') as file:
        n, capacity = map(int, file.readline().strip().split())
        values = []
        weights = []

        for line in file:
            value, weight = map(int, line.strip().split())
            values.append(value)
            weights.append(weight)

    return values, weights, capacity


values, weights, capacity = read_input_from_file('knapsack_problem.txt')
items = list(zip(values, weights))

maxProfit, selected_items = knapsack(items, capacity)
print("Максимальная прибыль:", maxProfit)
print("Выбранные предметы:", selected_items)
