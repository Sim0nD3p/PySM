import xml.etree.ElementTree as ET
from backend.PartCatalog import PartCatalog


class PartCatalogWriter:
    def __init__(self):
        self.test = 'string'

    @classmethod
    def save_default(cls, catalog):
        print('save catalog')
        catalog = PartCatalog().get_catalog()

        def scan(obj, element):

            if hasattr(obj, '__dict__'):
                for child in vars(obj):
                    new_element = ET.SubElement(element, child)
                    scan(vars(obj)[child], new_element)
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
        tree.write('backend/appData/catalog.xml')


