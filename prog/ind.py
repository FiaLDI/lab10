#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего индивидуального задания лабораторной работы 2.23 необходимо организовать
# конвейер, в котором сначала в отдельном потоке вычисляется значение первой функции,
# после чего результаты вычисления должны передаваться второй функции, вычисляемой в
# отдельном потоке. Потоки для вычисления значений двух функций должны запускаться
# одновременно.

import math
from threading import Barrier, Thread

E = 10e-7
results = [1]
br = Barrier(4)


def calculate_sum(x):
    return 3**x


def calculate_part(results, x, cur):
    local_result = [1]

    def my_log(local_result):
        local_result[0] *= math.pow(math.log(3), cur)
        br.wait()

    def my_pow(local_result):
        local_result[0] *= x**cur
        br.wait()

    def my_fact(local_result):
        local_result[0] /= math.factorial(cur)
        br.wait()

    Thread(target=my_log, args=(local_result,)).start()
    Thread(target=my_pow, args=(local_result,)).start()
    Thread(target=my_fact, args=(local_result,)).start()

    br.wait()
    results.append(local_result[0])


def main():
    x = 3
    i = 0
    while results[i] > E:
        calculate_part(results, x, i + 1)
        i += 1

    print(results)
    print(f"x = {x}")
    print(round(sum(results), 5))
    print(round(sum(results), 5) == calculate_sum(x))


if __name__ == "__main__":
    main()
