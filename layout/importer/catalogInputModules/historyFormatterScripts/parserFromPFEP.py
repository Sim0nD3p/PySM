import json
import math
from elements.part.usage.usageDataClasses import Order, Date


def number_to_int(number):
    """
    Transform value number to integer (int)
    :param number: number value (str, int, float)
    :return: int
    """
    if type(number) is str:
        if ',' in number:
            number = number.replace(',', '.')

        number = float(number)
        if math.isnan(number):
            return None # error - cannot convert to number
        number = int(math.ceil(number))

    return number


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
                        date = None
                        quantity = None
                        if number_to_int(year) and number_to_int(month) and number_to_int(day):
                            date = Date(number_to_int(year), number_to_int(month), number_to_int(day))
                        if number_to_int(child['history'][year][month][day]):
                            quantity = number_to_int(child['history'][year][month][day])

                        if date and quantity:
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









