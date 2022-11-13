import json
import csv

with open('schedule.json', encoding='utf-8') as file:
    source = file.read()
file.close()

parsed = json.loads(source)

with open('schedule.csv', 'w', encoding='utf-8') as file:
    w = csv.DictWriter(file, parsed.keys())
    w.writeheader()
    w.writerow(parsed)
