'''
1. Проанализировать скорость и сложность одного любого алгоритма из разработанных
в рамках домашнего задания первых трех уроков.
Примечание. Идеальным решением будет:
a. выбрать хорошую задачу, которую имеет смысл оценивать,
b. написать 3 варианта кода (один у вас уже есть),
c. проанализировать 3 варианта и выбрать оптимальный,
d. результаты анализа вставить в виде комментариев в файл с кодом
(не забудьте указать, для каких N вы проводили замеры),
e. написать общий вывод: какой из трёх вариантов лучше и почему.

Примечание по профилированию кода: для получения достоверных результатов при замере
времени необходимо исключить/заменить функции print() и input() в анализируемом коде.
С ними вы будете замерять время вывода данных в терминал и время, потраченное пользователем,
на ввод данных, а не быстродействие самого алгоритма.
'''
'''
5. В массиве найти максимальный отрицательный элемент.
Вывести на экран его значение и позицию в массиве.
Примечание к задаче: пожалуйста не путайте «минимальный»
 «максимальный отрицательный».
Это два абсолютно разных значения.
'''
import random
import cProfile


# Вычисление максимального элемента из всех отрицательных через один список без использования встроенных функций
def max_neg1(a_max_size, a):
    inf = float('inf')
    max_neg_elem = -inf
    max_neg_elem_i = -inf
    for i, elem in enumerate(a):
        if elem < 0 and elem > max_neg_elem:
            max_neg_elem = elem
            max_neg_elem_i = i
    if max_neg_elem > -inf:
        return (max_neg_elem_i, max_neg_elem)


# max_neg1(10)
# 1000 loops, best of 5: 21.7 usec per loop
# max_neg1(100)
# 1000 loops, best of 5: 200 usec per loop
# max_neg1(500)
# 1000 loops, best of 5: 1.02 msec per loop
# max_neg1(1000)
# 1000 loops, best of 5: 2.06 msec per loop

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# cProfile.run('max_neg1(10)')
# 55 function calls in 0.000 seconds
# 1    0.000    0.000    0.000    0.000 les4_task1.py:23(max_neg1)
# cProfile.run('max_neg1(100)')
# 505 function calls in 0.000 seconds
# 1    0.000    0.000    0.000    0.000 les4_task1.py:23(max_neg1)
# cProfile.run('max_neg1(500)')
# 2519 function calls in 0.002 seconds
# 1    0.000    0.000    0.001    0.001 les4_task1.py:23(max_neg1)
# cProfile.run('max_neg1(1000)')
# 5033 function calls in 0.004 seconds
# 1    0.000    0.000    0.004    0.004 les4_task1.py:23(max_neg1)

# Вычисление максимального элемента из всех отрицательных через один словарь без использования встроенных функций
def max_neg2(a):
    inf = float('inf')
    max_neg_elem = -inf
    max_neg_elem_i = -inf

    for i, elem in a.items():
        if elem < 0 and elem > max_neg_elem:
            max_neg_elem = elem
            max_neg_elem_i = i
    if max_neg_elem > -inf:
        return (max_neg_elem_i, max_neg_elem)


# max_neg2(10)
# 1000 loops, best of 5: 21.2 usec per loop
# max_neg2(100)
# 1000 loops, best of 5: 199 usec per loop
# max_neg1(500)
# 1000 loops, best of 5: 1.08 msec per loop
# max_neg2(1000)
# 1000 loops, best of 5: 2.11 msec per loop

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# cProfile.run('max_neg2(10)')
# 56 function calls in 0.000 seconds
# 1    0.000    0.000    0.000    0.000 les4_task1.py:61(max_neg2)
# cProfile.run('max_neg2(100)')
# 506 function calls in 0.001 seconds
# 1    0.000    0.000    0.000    0.000 les4_task1.py:61(max_neg2)
# cProfile.run('max_neg2(500)')
# 2521 function calls in 0.001 seconds
# 1    0.000    0.000    0.001    0.001 les4_task1.py:61(max_neg2)
# cProfile.run('max_neg2(1000)')
# 5036 function calls in 0.004 seconds
# 1    0.000    0.000    0.004    0.004 les4_task1.py:61(max_neg2)

# Вычисление максимального элемента из всех отрицательных через два списка с использованием встроенной функции max()
def max_neg3(a_max_size, a):
    b = [value for value in a if value < 0]

    if len(b) > 0:
        max_neg_elem = max(b)
        for i, elem in enumerate(a):
            if elem == max_neg_elem:
                max_neg_elem_i = i
        if a_max_size > 0:
            return (max_neg_elem_i, max_neg_elem)
    else:
        return None


# max_neg3(10)
# 1000 loops, best of 5: 21.4 usec per loop
# max_neg3(100)
# 1000 loops, best of 5: 204 usec per loop
# max_neg3(500)
# 1000 loops, best of 5: 1.1 msec per loop
# max_neg3(1000)
# 1000 loops, best of 5: 2.26 msec per loop

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# cProfile.run('max_neg3(10)')
# 59 function calls in 0.000 seconds
# 1    0.000    0.000    0.000    0.000 les4_task1.py:99(max_neg3)
# cProfile.run('max_neg3(100)')
# 513 function calls in 0.000 seconds
# 1    0.000    0.000    0.000    0.000 les4_task1.py:99(max_neg3)
# cProfile.run('max_neg3(500)')
# 2518 function calls in 0.002 seconds
# 1    0.000    0.000    0.002    0.002 les4_task1.py:99(max_neg3)
# cProfile.run('max_neg3(1000)')
# 5025 function calls in 0.004 seconds
# 1    0.000    0.000    0.004    0.004 les4_task1.py:99(max_neg3)

# Вычисление максимального элемента из всех отрицательных через два списка с использованием рекурсивной функции
def max2(L):
    if len(L) == 1:
        return L[0]
    mid = (len(L)) // 2
    left_L = [L[i] for i in range(0, mid)]
    right_L = [L[i] for i in range(mid, len(L))]
    a = max2(left_L)
    b = max2(right_L)
    return max(a, b)


def main(a_max_size):
    a = [random.randint(-1000, 1000) for i in range(0, a_max_size)]
    b = [value for value in a if value < 0]

    if len(b) > 0:
        max_neg_elem = max2(b)
        for i, elem in enumerate(a):
            if elem == max_neg_elem:
                max_neg_elem_i = i
        return (max_neg_elem_i, max_neg_elem)


# main(10)
# 1000 loops, best of 5: 31.4 usec per loop
# main(100)
# 1000 loops, best of 5: 339 usec per loop
# main(500)
# 1000 loops, best of 5: 1.85 msec per loop
# main(1000)
# 1000 loops, best of 5: 3.75 msec per loop

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# cProfile.run('main(10)')
# 105 function calls (95 primitive calls) in 0.000 seconds
# 11/1    0.000    0.000    0.000    0.000 les4_task1.py:137(max2)
# cProfile.run('main(100)')
# 1005 function calls (895 primitive calls) in 0.000 seconds
# 111/1    0.000    0.000    0.000    0.000 les4_task1.py:137(max2)
# cProfile.run('main(500)')
# 4679 function calls (4199 primitive calls) in 0.003 seconds
# 481/1    0.001    0.000    0.002    0.002 les4_task1.py:137(max2)
# cProfile.run('main(1000)')
# 9668 function calls (8638 primitive calls) in 0.007 seconds
# 1031/1    0.002    0.000    0.003    0.003 les4_task1.py:137(max2)

'''Можно сделать вывод, что функция работает одинаково через список и через словарь, такие же результаты
функция показала при нахождении максимума через встроенную функцию. Рекурсивный вариант выполняется дольше.
На графике построены зависимости t(n) для функций max_neg1 и main+max2 т.к. max_neg2 и max_neg3 на таком масштабе 
будут сливаться с max_neg1. На графике видно что функции имеют зависимость О(n) с той лишь разницей, что рекурсивная 
зависимость имеет больший угол наклона'''
