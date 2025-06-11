import re
import csv

f = open('row.txt', 'r', encoding='utf8')
text = f.read()

pattern = r"\n(?P<номер>[0-9]+)\.\n(?P<название>.+)\n(?P<количество>.+)x(?P<цена>.+)\n(?P<стоимость>.+)"

res = re.finditer(pattern, text)

with open('data.csv', 'w', newline='',encoding="utf8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['номер', 'название', 'количество', 'цена', 'стоимость'])
    for x in res:
        writer.writerow([
            x.group('номер'), 
            x.group('название'),
            float(x.group('количество').strip().replace(',','.')),
            float(x.group('цена').strip().replace(',','.').replace(' ','')),
            float(x.group('стоимость').strip().replace(',','.').replace(' ',''))
        ])