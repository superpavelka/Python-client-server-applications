"""Unit-тесты сервера"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, LOGIN, TIME, ACTION, PRESENCE
from server import process_client_message

class TestServer(unittest.TestCase):
    '''
    В сервере только 1 функция для тестирования
    '''
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request - Сервер не понимает запрос из-за неверного синтаксиса'
    }

    ok_dict = {RESPONSE: 200}

    def test_no_action(self):
        """Ошибка если нет действия"""
        self.assertEqual(process_client_message(
            {TIME: '0', USER: {LOGIN: 'Guest'}}), self.err_dict)

    def test_no_action_wrong_ans(self):
        """Ошибка если нет действия"""
        self.assertNotEqual(process_client_message(
            {TIME: '0', USER: {LOGIN: 'Guest'}}), self.ok_dict)

    def test_wrong_action(self):
        """Ошибка если неизвестное действие"""
        self.assertEqual(process_client_message(
            {ACTION: 'BAD_ACTION', TIME: '0', USER: {LOGIN: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {LOGIN: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '0'}), self.err_dict)

    def test_unknown_user(self):
        """Ошибка - не Guest"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 0, USER: {LOGIN: 'Guest1'}}), self.err_dict)

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 0, USER: {LOGIN: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()