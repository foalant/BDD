from dd.autoref import BDD
import sys

def create_queen_bdd(n):
    bdd = BDD()
    bdd.declare(*['Q_{}_{}'.format(i, j) for i in range(n) for j in range(n)])
    
    def exactly_one(vars):
        return bdd.add_expr("({}) & {}".format(' | '.join(vars), ' & '.join(['~({} & {})'.format(v1, v2) for i, v1 in enumerate(vars) for v2 in vars[i+1:]])))
    
    # Создаем начальную формулу
    bdd_formula = bdd.true

    # Ограничение: одна ферзь на каждой строке
    for i in range(n):
        row_vars = ['Q_{}_{}'.format(i, j) for j in range(n)]
        bdd_formula &= exactly_one(row_vars)

    # Ограничение: одна ферзь на каждом столбце
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

def print_solutions(bdd, bdd_formula, n, max_solutions=10):
    solutions = bdd.pick_iter(bdd_formula)
    count = 0
    for sol in solutions:
        if count >= max_solutions:
            break
        board = [['.' for _ in range(n)] for _ in range(n)]
        for var, val in sol.items():
            if val:
                i, j = map(int, var[2:].split('_'))
                board[i][j] = 'Q'
        for row in board:
            print(' '.join(row))
        print('')
        count += 1
    if count == 0:
        print("No solutions found")

def main():
    # Запрос размера доски у пользователя
    while True:
        try:
            if sys.version_info[0] < 3:
                n = int(raw_input("Введите размер шахматной доски (целое число): "))
            else:
                n = int(input("Введите размер шахматной доски (целое число): "))
            if n <= 0:
                raise ValueError("Размер доски должен быть положительным целым числом.")
            break
        except ValueError as e:
            print("Ошибка: ", e)

    # Создание BDD и решение задачи о размещении ферзей
    bdd, bdd_formula = create_queen_bdd(n)
    # Выводим не более 10 решений
    print_solutions(bdd, bdd_formula, n, max_solutions=10)

if __name__ == "__main__":
    main()
