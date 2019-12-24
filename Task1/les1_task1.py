'''
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип
и содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые
представление в формат Unicode и также проверить тип и содержимое переменных.
'''

WORDS = []
WORDS.append('разработка')
WORDS.append('сокет')
WORDS.append('декоратор')

for word in WORDS:
    print(word)
    print(type(word))

WORDS.clear()
WORDS.append('\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430')
WORDS.append('\u0441\u043e\u043a\u0435\u0442')
WORDS.append('\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440')

for word in WORDS:
    print(word)
    print(type(word))
