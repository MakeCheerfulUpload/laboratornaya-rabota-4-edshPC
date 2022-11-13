import json
from dicttoxml import dicttoxml

file = open('schedule.json', encoding='utf-8')
source = file.read()
file.close()

parsed = json.loads(source)
print('Словарь из JSON:', parsed)

rawXML = dicttoxml(parsed, attr_type=False).decode('utf-8')
print('В XML:', rawXML)

file = open('schedule.xml', 'w', encoding='utf-8')
file.write(rawXML)
file.close()
