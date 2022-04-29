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

        for xml_store_object in xml.getroot():
            properties = xml_store_object.attrib
            racking = None

            # Defining RACKING
            if properties['type'] == RACKING:
                racking = Racking.init_from_xml(xml_store_object)    # initiate racking from xml xml_store_object
                print('racking')

                # Looping for shelves
                for xml_shelf in xml_store_object:
                    if 'type' in xml_shelf.attrib:
                        shelf = None
                        if xml_shelf.attrib['type'] == FLAT_SHELF:
                            shelf = FlatShelf.init_from_xml(xml_shelf)
                        else:
                            # TODO handle other types of shelves
                            pass

                        if shelf:
                            for xml_so in xml_shelf:
                                so = StorageObject.init_from_xml(xml_so)
                                shelf.add_storage(so)

                            racking.add_shelf(shelf)
            else:
                # TODO handle other types of store object
                pass



            StoreFloor.add_object(racking)





