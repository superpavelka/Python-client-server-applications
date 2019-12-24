'''
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode).
'''

WORDS = []
WORDS.append('разработка')
WORDS.append('администрирование')
WORDS.append('protocol')
WORDS.append('standard')

for word in WORDS:
    word = str.encode(word, encoding='utf-8')
    print(word)
    print(type(word))
    word = bytes.decode(word, encoding='utf-8')
    print(word)
    print(type(word))
