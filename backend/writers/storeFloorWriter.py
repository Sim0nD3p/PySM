import xml.etree.ElementTree as et
from backend.storeFloor import StoreFloor, StoreObject
from elements.elementsTypes import *
from elements.racking.racking import Racking
import numpy as np
from elements.ElementLogic.containerPlacement import *


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
                    # print(shelf.geometry)
                    # print('geo', geo)
                    # print('shelf', vars(shelf))
                    xml_shelf = et.SubElement(xml_element,
                                              'shelf',
                                              attrib={
                                                  'name': shelf.name,
                                                  'id': str(shelf.id),
                                                  'type': shelf.type,
                                                  'geometry': geo
                                              })
                    for so in shelf.storage_objects:
                        print('storage object')
                        geo = np.array2string(so.geometry.flatten())
                        # get placement name
                        print('so.placement_cb', so.placement)
                        placement_name = ''
                        if so.placement:
                            print('should get placement name')
                            placement_name = ContainerPlacement.get_placement_name(placement=so.placement)


                        xml_so = et.SubElement(xml_shelf,
                                               'storage_object',
                                               attrib={
                                                   'part_code': str(so.part_code),
                                                   'geo': geo,
                                                   'placement': placement_name,
                                                   'parent_shelf_id': str(so.parent_shelf_id),
                                               })
                        for cont in so.containers:
                            geo = np.array2string(cont.geometry.flatten())
                            attrib = {
                                'name': cont.name,
                                'geo': geo,
                                'stored_part': str(cont.stored_part),
                                'content': np.array2string(cont.content.flatten()),
                            }
                            xml_cont = et.SubElement(xml_so,
                                                     cont.type,
                                                     attrib=attrib
                                                     )



            xml_element.text = 'test'




        tree = et.ElementTree(xml_root)
        tree.write('backend/appData/storeFloor.xml')


