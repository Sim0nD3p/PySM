import xml.etree.ElementTree as ET
from backend.PartCatalog import PartCatalog


class PartCatalogWriter():
    def __init__(self):
        self.test = 'string'

    @classmethod
    def save_default(cls, catalog):
        print('save catalog')
        catalog = PartCatalog().get_catalog()

        def scan(obj, element):
            # print('obj', obj)
            if hasattr(obj, '__dict__'):
                for child in vars(obj):
                    print('child: content')
                    print(child, ':', vars(obj)[child])
                    new_element = ET.SubElement(element, child)
                    scan(vars(obj)[child], new_element)
            else:

                # print('has no __dict__')
                # print(obj, type(obj))
                if type(obj) == dict:
                    for child in obj:
                        # print('child', child)
                        # print('obj[child]', obj[child])
                        print(child, obj[child])
                        new_element = ET.SubElement(element, child)
                        scan(obj[child], new_element)
                else:
                    print(element)
                    element.text = obj
                    print(obj)

        xml = ET.Element('root')

        for part in catalog:
            part_element = ET.SubElement(xml, 'part', attrib={'code': part.code})
            scan(part, part_element)
        # scan(catalog[0], xml)

        tree = ET.ElementTree(xml)
        tree.write('test2.xml')


