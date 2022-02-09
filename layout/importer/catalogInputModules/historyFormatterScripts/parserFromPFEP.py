import json
from part.usage.usageDataClasses import Order, Date
import xml.etree.ElementTree as ET
from layout.importer.catalogInputModules.historyFormatterScripts.suppInfos import suppliers

def parseFromPFEP(file_path):
    orders = []
    print('value')
    with open(file_path, 'r') as json_string:
        json_data = json.load(json_string)
        for child in json_data:
            suppliers = child['supplier']
            supplier_name = 'None'
            if len(suppliers) >= 1:
                supplier_name = suppliers[0]['name']
            current_part = child['code']
            # print(child['code'])
            for year in child['history']:
                for month in child['history'][year]:
                    for day in child['history'][year][month]:
                        date = Date(year, month, day)
                        quantity = child['history'][year][month][day]
                        o = Order(current_part, date, quantity, supplier_name)
                        orders.append(o)
        return orders


# creating pool of all orders

# write xml
"""
dsa

root = ET.Element('orders')
xml = ET.ElementTree(root)
root = ET.SubElement(root, 'order')
orders = []
for order in orders:
    print(order)
    o = ET.SubElement(root, 'order')

    part_code = ET.SubElement(o, 'code')
    part_code.text = order.part_code

    date = ET.SubElement(o, 'date')

    year = ET.SubElement(date, 'year')
    year.text = order.date.year

    month = ET.SubElement(date, 'month')
    month.text = order.date.month

    day = ET.SubElement(date, 'day')
    day.text = order.date.day

    quantity = ET.SubElement(o, 'quantity')
    quantity.text = order.quantity

    supplier = ET.SubElement(o, 'supplier')
    supplier.text = order.supplier_name

xml.write('../../../../backend/appData/privateData/orders.xml')
"""









