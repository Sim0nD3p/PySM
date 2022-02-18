import xml.etree.ElementTree as ET
from backend.PartCatalog import PartCatalog
from part.usage.usageDataClasses import Order, Date
from part.Part import Part
from layout.settings.settings import Settings


class PartCatalogLoader:

    @staticmethod
    def create_orders_pool_from_xml(xml_element):
        """
        Makes list of order
        :param xml_element: part xml element
        :return: Order objects list (order_pool)
        """
        pool = []
        for order in xml_element.find('orders'):
            part_code = order.find('part_code').text
            date_elements = order.find('date').text.split('-')
            date = Date(int(date_elements[0]), int(date_elements[1]), int(date_elements[2]))
            supplier_name = order.find('supplier').text
            quantity = int(order.find('quantity').text)
            pool.append(Order(part_code, date, quantity, supplier_name))

        return pool


    @classmethod
    def load_xml_catalog(cls, file):
        """
        Loads PartCatalog from xml file
        instructions on how to load the file is in a xml file
        1. For each part element of xml file, does loop to create object
        2. Check if object is in PartCatalog if not, adds orders to order_history and adds part to PartCatalog
        :param file: file path for xml catalog
        :return: void
        """
        xml_object = ET.ElementTree()
        xml_object.parse(file)
        root = xml_object.getroot()

        def create_object(data, instructions):
            """
            Creates object with properties and data from data and instructions
            :param data: data dict
            :param instructions: instructions dict
            :return: Part Object
            """
            part_code = Part.get_code(data, instructions)
            new_part = Part(part_code)
            new_part.general_information = Part.make_general_information(data, instructions)
            new_part.specifications = Part.make_specifications(data, instructions)
            new_part = Part.add_custom_prop(new_part, data, instructions)
            return new_part

        # getting instructions on object structure/instructions in part_model
        default_xml_tree = ET.ElementTree()
        file = Settings.part_model_path  # file on how to get instructions
        default_xml_tree.parse(file)       # parsing instructions
        instructions_root = default_xml_tree.getroot()  # getting root of instructions
        decoder_instructions = Part.inspect_xml_tree(instructions_root)

        imported_list = []
        for part_xml_element in root:
            part = create_object(Part.inspect_xml_tree(part_xml_element), decoder_instructions)  # create part
            if not PartCatalog.check_presence(part):    # check if part is in PartCatalog
                # add orders to part.order_history
                part.add_orders_to_history(PartCatalogLoader.create_orders_pool_from_xml(part_xml_element))
                PartCatalog.add_part(part)  # add part to catalog
        print('catalog now has', len(PartCatalog.catalog))




