import xml.etree.ElementTree as et
from backend.storeFloor import StoreFloor, StoreObject
from elements.elementsTypes import *
from elements.racking.racking import Racking
from elements.shelf.shelf import *
from elements.shelf.flatShelf import *

class StoreFloorLoader:
    def __init__(self):
        self.version = 1

    @staticmethod
    def load_floor_from_xml(file_path):
        xml = et.ElementTree()
        xml.parse(file_path)

        for element in xml.getroot():
            properties = element.attrib
            if properties['type'] == RACKING:
                racking = Racking.init_from_xml(element)    # initiate racking from xml element
                print('racking')

                for xml_shelf in element:
                    if 'type' in xml_shelf.attrib:
                        if xml_shelf.attrib['type'] == FLAT_SHELF:
                            shelf = FlatShelf.init_from_xml(xml_shelf)
                            if shelf:
                                racking.add_shelf(shelf)

                StoreFloor.add_object(racking)




