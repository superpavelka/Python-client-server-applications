'''
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования
в последовательность кодов (не используя методы encode и decode) и определить тип, содержимое
и длину соответствующих переменных.
'''
WORDS = []
WORDS.append(b'class')
WORDS.append(b'function')
WORDS.append(b'method')

for word in WORDS:
    print(word)
    print(type(word))
    print(len(word))
