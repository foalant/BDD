from dd.autoref import BDD
import sys


def create_queen_bdd(n):
    bdd = BDD()
    bdd.declare(*['Q_{}_{}'.format(i, j) for i in range(n) for j in range(n)])

    def exactly_one(vars):
        return bdd.add_expr("({}) & {}".format(
            ' | '.join(vars),
            ' & '.join(['~({} & {})'.format(v1, v2) for i, v1 in enumerate(vars) for v2 in vars[i + 1:]])
        ))

    # Начальная формула
    bdd_formula = bdd.true

    # Ограничения для ферзей
    # Ограничение: один ферзь на каждой строке
    for i in range(n):
        row_vars = ['Q_{}_{}'.format(i, j) for j in range(n)]
        bdd_formula &= exactly_one(row_vars)

    # Ограничение: один ферзь на каждом столбце
    for j in range(n):
        col_vars = ['Q_{}_{}'.format(i, j) for i in range(n)]
        bdd_formula &= exactly_one(col_vars)

    # Ограничение: ферзи не атакуют друг друга по диагоналям
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    if abs(i - k) == abs(j - l) and (i != k or j != l):
                        bdd_formula &= bdd.add_expr('~Q_{}_{} | ~Q_{}_{}'.format(i, j, k, l))

    return bdd, bdd_formula


def create_graph_coloring_bdd(n, k):
    bdd = BDD()

    # Объявляем переменные для раскраски графа
    bdd.declare(*['C_{}_{}'.format(i, j) for i in range(n) for j in range(k)])

    # Начальная формула (все условия)
    bdd_formula = bdd.true

    # Функция для ограничения: один цвет для каждой вершины
    def exactly_one(vars):
        return bdd.add_expr("({}) & {}".format(
            ' | '.join(vars),
            ' & '.join(['~({} & {})'.format(v1, v2) for i, v1 in enumerate(vars) for v2 in vars[i + 1:]])
        ))

    # Ограничение: для каждой вершины должен быть использован ровно один цвет
    for i in range(n):
        vars = ['C_{}_{}'.format(i, j) for j in range(k)]
        bdd_formula &= exactly_one(vars)

    # Ограничение: соседи не могут иметь одинаковый цвет
    for i in range(n):
        for j in range(i + 1, n):  # Проверяем каждую пару вершин
            for c in range(k):
                bdd_formula &= bdd.add_expr('~C_{}_{} | ~C_{}_{}'.format(i, c, j, c))

    return bdd, bdd_formula


def print_solutions(bdd, bdd_formula, n, k=None, max_solutions=10):
    solutions = bdd.pick_iter(bdd_formula)
    count = 0
    for sol in solutions:
        if count >= max_solutions:
            break
        if k is None:  # Если задача о ферзях
            board = [['.' for _ in range(n)] for _ in range(n)]
            for var, val in sol.items():
                if val:
                    i, j = map(int, var[2:].split('_'))
                    board[i][j] = 'Q'
            for row in board:
                print(' '.join(row))
            print('')
        else:  # Если задача о раскраске графа
            for i in range(n):
                for j in range(k):
                    if sol['C_{}_{}'.format(i, j)]:
                        print(f"Vertex {i}: Color {j}")
            print('---')
        count += 1
    if count == 0:
        print("No solutions found")


def main():
    # Выбор задачи
    task_choice = input("Выберите задачу (1 - Ферзи, 2 - Раскраска графа): ")

    if task_choice == '1':
        # Запрос размера доски
        while True:
            try:
                n = int(input("Введите размер шахматной доски (целое число): "))
                if n <= 0:
                    raise ValueError("Размер доски должен быть положительным целым числом.")
                break
            except ValueError as e:
                print("Ошибка: ", e)

        # Создание BDD и решение задачи о размещении ферзей
        bdd, bdd_formula = create_queen_bdd(n)
        print_solutions(bdd, bdd_formula, n, max_solutions=20)

    elif task_choice == '2':
        # Запрос количества вершин графа
        while True:
            try:
                n = int(input("Введите количество вершин графа (целое число): "))
                if n <= 0:
                    raise ValueError("Количество вершин должно быть положительным целым числом.")
                break
            except ValueError as e:
                print("Ошибка: ", e)

        # Запрос количества цветов для раскраски
        while True:
            try:
                k = int(input("Введите количество цветов для раскраски (целое число): "))
                if k <= 0:
                    raise ValueError("Количество цветов должно быть положительным целым числом.")
                break
            except ValueError as e:
                print("Ошибка: ", e)

        # Создание BDD и решение задачи раскраски графа
        bdd, bdd_formula = create_graph_coloring_bdd(n, k)
        print_solutions(bdd, bdd_formula, n, k, max_solutions=20)


if __name__ == "__main__":
    main()
