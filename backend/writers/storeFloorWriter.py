import xml.etree.ElementTree as et
from backend.storeFloor import StoreFloor, StoreObject
from elements.elementsTypes import *
from elements.racking.racking import Racking
import numpy as np


class StoreFloorWriter:
    """"
    for all object in StoreFloor, write properties accordignly

    """
    def __init__(self):
        self.version = 1

    @classmethod
    def save_default(cls, store_floor: StoreFloor):
        """
        name
        id
        geometry_matrix
        :param store_floor:
        :return:
        """
        print('saving storeFloor')
        xml_root = et.Element('root')
        for element in store_floor.objects:
            geometry_buffer = element.geometry.tobytes()
            geo = np.array2string(element.geometry.flatten())

            xml_element = et.SubElement(xml_root,
                                        'object',
                                        attrib={
                                            'name': element.name,
                                            'type': element.type,
                                            'id': str(element.id),
                                            'geometry': geo

                                        })

            if type(element) == Racking:
                for shelf in element.shelves:
                    geo = np.array2string(shelf.geometry.flatten())
                    print(shelf.geometry)
                    print('geo', geo)
                    print('shelf', vars(shelf))
                    et.SubElement(xml_element,
                                  'shelf',
                                  attrib={
                                      'name': shelf.name,
                                      'id': str(shelf.id),
                                      'type': shelf.type,
                                      'geometry': geo
                                  }
                                  )


            xml_element.text = 'test'




        tree = et.ElementTree(xml_root)
        tree.write('backend/appData/storeFloor.xml')


