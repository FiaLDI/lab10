#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего индивидуального задания лабораторной работы 2.23
# необходимо организовать конвейер, в котором сначала в
# отдельном потоке вычисляется значение первой функции,
# после чего результаты вычисления должны передаваться
# второй функции, вычисляемой в отдельном потоке.
# Потоки для вычисления значений двух функций должны запускаться
# одновременно.

# Вариант 1 и 2

import math
from threading import Lock, Thread

E = 10e-7

lock_obj = Lock()


# 1 Вариант
def calculate_row_1(target, x):
    def calculate_nextpart(results, x, cur):
        return results[-1] * x * math.log(3) / cur

    i = 0

    local_result = [1]
    while local_result[i] > E:
        local_result.append(calculate_nextpart(local_result, x, i + 1))
        i += 1

    with lock_obj:
        target["sum_row_1"] = sum(local_result)


# 2 Вариант
def calculate_row_2(target, x):
    def calculate_nextpart(results, x):
        return results[-1] * x

    i = 0
    local_result = [1]
    while local_result[i] > E:
        local_result.append(calculate_nextpart(local_result, x))
        i += 1

    with lock_obj:
        target["sum_row_2"] = sum(local_result)


def check_results(target, x1, x2):
    with lock_obj:

        def control_value_1(x):
            return 3**x

        def control_value_2(x):
            return round(1 / (1 - x), 4)

        print(
            f'Различие найденной суммы с контрольным значением /n
                {control_value_1(x1) - target.get("sum_row_1")}'
        )
        print(
            f'Различие найденной суммы с контрольным значением /n
                {control_value_2(x2) - target.get("sum_row_2")}'
        )
        print(f"Результат {target}")


def main():
    part_of_rows = {"sum_row_1": 0, "sum_row_2": 0}

    th1 = Thread(target=calculate_row_1, args=(part_of_rows, 1))
    th2 = Thread(target=calculate_row_2, args=(part_of_rows, 0.7))
    th3 = Thread(target=check_results, args=(part_of_rows, 1, 0.7))

    th1.start()
    th2.start()
    th3.start()


if __name__ == "__main__":
    main()
