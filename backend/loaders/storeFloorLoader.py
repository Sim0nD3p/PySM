import xml.etree.ElementTree as et
from backend.storeFloor import StoreFloor, StoreObject
from elements.elementsTypes import *
from elements.racking.racking import Racking

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
                print('racking')
                racking = Racking.init_from_xml(element)
                StoreFloor.add_object(racking)




