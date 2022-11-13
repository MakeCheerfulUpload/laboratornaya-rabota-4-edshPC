def splitDict(source):
    out = []
    temp = ''
    level = 0
    inQuotes = False
    for char in source:
        if char == '"':
            inQuotes = not inQuotes
        elif char in '{[':
            level += 1
        elif char in '}]':
            level -= 1

            # Если не запятая, либо мы внутри скобок, либо внутри кавычек продолжаем набирать строку
        if level > 0 or inQuotes or char != ',':
            temp += char
        else:
            out.append(temp)
            temp = ''
    out.append(temp)
    return out


def getDictFromStr(source):
    outStr = source[0] + source[-1]
    inStr = source[1:-1]
    if outStr == '{}':
        if inStr == '':
            return {}
        tempDict = {}
        for keyVal in splitDict(inStr):
            # Разделяем ключ-значение (ключ в кавычках), значение не отделяем
            key, val = keyVal.split(':', 1)
            tempDict[key[1:-1]] = getDictFromStr(val)
        return tempDict

    if outStr == '[]':
        if inStr == '':
            return []
        #Генерируем массив из значений через запятую
        return [getDictFromStr(x) for x in splitDict(inStr)]

    if outStr == '""':
        return inStr
    try:
        x = int(source)
        return x
    except:
        pass
    try:
        x = float(source)
        return x
    except:
        pass
    if source == 'true':
        return True
    if source == 'false':
        return False
    return None


def parseJson(source, needPrint = True):
    inQuotes = False
    rawJson = ''
    # Убираем все лишние пробелы и переносы строк
    for char in source:
        if char == '"':
            inQuotes = not inQuotes
        if char not in ' \n' or inQuotes:
            rawJson += char
    if needPrint:
        print('Сжатый JSON:', rawJson)
    return getDictFromStr(rawJson)


def toXMLstring(source, lastKey='element'):
    #Если пришло значение просто переводим в строку
    if type(source) in [str, int, float]:
        return str(source)
    if type(source) is bool:
        return str(source).lower()

    #Доп. функция чтобы Записывать ключ по бокам от значения и продолжать рекурсивно получать значение
    def getAddRes(key, val):
        tempVal = toXMLstring(val, key)
        isList = type(val) is list
        if tempVal is None:
            if isList:
                return ''
            else:
                return '<' + key + ' />'

        if isList:
            return tempVal
        return '<' + key + '>' + tempVal + '</' + key + '>'

    #Если попал словарь (с ключём) передаем отдельно ключ и значение
    if type(source) is dict:
        if len(source) == 0:
            return
        res = ''
        for key, val in source.items():
            res += getAddRes(key, val)
        return res

    #Если попал лист (массив без ключей) передаем предыдущий запомненный ключ, так устроен XML
    if type(source) is list:
        if len(source) == 0:
            return
        res = ''
        for elem in source:
            res += getAddRes(lastKey, elem)
        return res


file = open('schedule.json', encoding='utf-8')
source = file.read()
file.close()

parsed = parseJson(source)
print('Словарь из JSON:', parsed)
rawXML = toXMLstring(parsed)
print('В XML:', rawXML)
rawXML = '<?xml version="1.0" encoding="UTF-8" ?><root>' + rawXML + '</root>'

file = open('schedule.xml', 'w', encoding='utf-8')
file.write(rawXML)
file.close()
print('TEST')