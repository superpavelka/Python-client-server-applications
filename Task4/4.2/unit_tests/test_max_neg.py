"""Unit-тесты max_neg"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from max_neg import max_neg1, max_neg2, max_neg3


class TestClass(unittest.TestCase):
    '''
    Класс с тестами
    '''

    def test_max_neg1(self):
        """Тест массива от 0 до -99 функции max_neg1"""
        array = [-1 * i for i in range(0, 100)]
        self.assertEqual(max_neg1(100, array), (1, -1))

    def test_max_neg2(self):
        """Тест массива от 98 до -1 функции max_neg2"""
        map_ = {i: -1 * (i - 98) for i in range(0, 100)}
        self.assertEqual(max_neg2(map_), (99, -1))

    def test_max_neg3(self):
        """Тест массива от 99 до 0 функции max_neg3"""
        array = [-1 * (i - 99) for i in range(0, 100)]
        self.assertEqual(max_neg3(100, array), None)


if __name__ == '__main__':
    unittest.main()
