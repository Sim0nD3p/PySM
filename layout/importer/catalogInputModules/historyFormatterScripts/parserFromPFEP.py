import json
from part.usage.usageDataClasses import Order, Date
from layout.importer.catalogInputModules.historyFormatterScripts.suppInfos import suppliers

print('parsing from PFEP.json')

file_path = 'C:/Users/simon/Documents/Techno-Fab/PySM/PySM/PFEPtest.json'

orders = []

with open(file_path, 'r') as json_string:
    json_data = json.load(json_string)
    for child in json_data:
        suppliers = child['supplier']
        supplier_name = 'None'
        if len(suppliers) >= 1:
            supplier_name = suppliers[0]['name']
        current_part = child['code']
        print(child['code'])
        for year in child['history']:
            for month in child['history'][year]:
                for day in child['history'][year][month]:
                    date = Date(year, month, day)
                    quantity = child['history'][year][month][day]
                    o = Order(current_part, date, quantity, supplier_name)
                    orders.append(o)


    for child in orders:
        print(child)


