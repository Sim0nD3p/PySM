import xml.etree.ElementTree as et
from backend.storeFloor import StoreFloor, StoreObject
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
            geometry_buffer = element.geometry_matrix.tobytes()
            geo = np.array2string(element.geometry_matrix.flatten())

            xml_element = et.SubElement(xml_root,
                                        'object',
                                        attrib={
                                            'name': element.name,
                                            'type': element.type,
                                            'id': str(element.id),
                                            'geometry': geo

                                        })

            xml_element.text = 'test'




        tree = et.ElementTree(xml_root)
        tree.write('backend/appData/storeFloor.xml')


