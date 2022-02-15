import xml.etree.ElementTree as ET
from backend.PartCatalog import PartCatalog


class PartCatalogWriter:
    def __init__(self):
        self.test = 'string'

    @classmethod
    def save_default(cls, catalog):
        print('save catalog')
        catalog = PartCatalog().get_catalog()
        exceptions = ['order_history']

        def convert_orders_xml(order_history, xml_parent_element):

            if hasattr(order_history, 'orders'):
                for order in order_history.orders:
                    order_element = ET.SubElement(xml_parent_element, 'order')
                    if hasattr(order, 'part_code') and hasattr(order, 'date') and hasattr(order, 'quantity'):

                        part_code = ET.SubElement(order_element, 'part_code')
                        part_code.text = order.part_code

                        date = ET.SubElement(order_element, 'date')
                        date.text = str(order.date.get_date())

                        quantity = ET.SubElement(order_element, 'quantity')
                        quantity.text = str(order.quantity)

                        supplier = ET.SubElement(order_element, 'supplier')
                        supplier.text = order.supplier_name



        def scan(obj, element):

            if hasattr(obj, '__dict__'):
                for child in vars(obj):
                    if child not in exceptions:
                        new_element = ET.SubElement(element, child)
                        scan(vars(obj)[child], new_element)
                    elif child == 'order_history':
                        new_element = ET.SubElement(element, 'orders')
                        convert_orders_xml(vars(obj)[child], new_element)

            else:

                if type(obj) == dict:
                    for child in obj:
                        new_element = ET.SubElement(element, child)
                        scan(obj[child], new_element)
                else:
                    element.text = str(obj)

        xml = ET.Element('root')

        for part in catalog:
            print('writing part:', part.code)
            part_element = ET.SubElement(xml, 'part', attrib={'code': part.code})
            scan(part, part_element)
        # scan(catalog[0], xml)


        tree = ET.ElementTree(xml)
        print(tree)
        tree.write('backend/appData/catalog_new.xml')


