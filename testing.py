from mainProgram import parseJson as parse_main
from mainProgram import toXMLstring as toXML_main

from json import loads
from dicttoxml import dicttoxml

from withRegex import parseJson as parse_regex
from withRegex import toXMLstring as toXML_regex
#Импорты вызывают основной код и мы его просто опустим
#На время тестов не повлиеят, тк таймер начинается позже
print('\n'*10)

file = open('schedule.json', encoding='utf-8')
source = file.read()
file.close()

import time
iters = 2000

start = time.time()
for i in range(iters):
    toXML_main(parse_main(source, needPrint=False))
print('На ручной парсинг ушло %s секунд' % (time.time()-start))

start = time.time()
for i in range(iters):
    dicttoxml(loads(source), attr_type=False).decode('utf-8')
print('На парсинг библиотеками ушло %s секунд' % (time.time()-start))

start = time.time()
for i in range(iters):
    toXML_regex(parse_regex(source, needPrint=False))
print('На парсинг регулярками ушло %s секунд' % (time.time()-start))