"""Unit-тесты клиента"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, LOGIN, TIME, ACTION, PRESENCE
from client import create_presence, process_ans


class TestClass(unittest.TestCase):
    '''
    Класс с тестами
    '''

    def test_def_presense(self):
        """Тест коректного запроса"""
        test = create_presence()
        test[TIME] = 0  # время необходимо приравнять принудительно
        # иначе тест никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 0, USER: {LOGIN: 'Guest'}})

    def test_def_presense_wrong_login(self):
        """Тест коректного запроса"""
        test = create_presence()
        test[TIME] = 0
        self.assertNotEqual(test, {ACTION: PRESENCE, TIME: 0, USER: {LOGIN: 'Anonymous'}})

    def test_ans_200(self):
        """Тест корректного разбора ответа 200"""
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK - Запрос выполнен успешно')

    def test_ans_200_wrong_ans(self):
        """Тест корректного разбора ответа 200"""
        self.assertNotEqual(process_ans({RESPONSE: 200}), '400 : Bad Request')

    def test_ans_400(self):
        """Тест корректного разбора 400"""
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_ans_400_wrong_ans(self):
        """Тест корректного разбора 400"""
        self.assertNotEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '200 : OK - Запрос выполнен успешно')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
