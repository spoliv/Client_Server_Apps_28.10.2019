import unittest
from HomeWorks.Lesson_4.common.constants import *
from HomeWorks.Lesson_4.client import show_presence, proc_answer


# Класс с тестами


class TestClass(unittest.TestCase):
    # тест коректного запроса
    def test_def_presense(self):
        test = show_presence()
        # время необходимо приравнять принудительно иначе тест никогда не будет
        # пройден
        test[TIME] = 1.1
        self.assertEqual(
            test, {
                ACTION: PRESENCE, TIME: 1.1, USER: {
                    ACCOUNT_NAME: 'Guest'}})

    # тест корректтного разбора ответа 200
    def test_200_ans(self):
        self.assertEqual(proc_answer({RESPONSE: 200}), '200 : OK')

    # тест корректного разбора 400
    def test_400_ans(self):
        self.assertEqual(proc_answer(
            {RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    # тест исключения без поля RESPONSE
    def test_no_response(self):
        self.assertRaises(ValueError, proc_answer, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
