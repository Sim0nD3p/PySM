import xml.etree.ElementTree as ET
from backend.PartCatalog import PartCatalog
from part.Part import Part


class PartCatalogLoader:

    @classmethod
    def load_xml_catalog(cls, file):
        xml_object = ET.ElementTree()
        xml_object.parse(file)
        root = xml_object.getroot()

        def scan(obj, root):
            for child in obj:
                print(child)


        def create_object(data, instructions):
            part_code = Part.get_code(data, instructions)
            # print(part_code)
            part = Part(part_code)
            part.general_information = Part.make_general_information(data, instructions)
            part.specifications = Part.make_specifications(data, instructions)
            # print(vars(part))
            return part

        default_xml_tree = ET.ElementTree()
        file = 'backend/appData/partModels/default_part_model.xml'  # file on how to get instructions
        default_xml_tree.parse(file)       # parsing instructions
        instructions_root = default_xml_tree.getroot()  # getting root of instructions
        decoder_instructions = Part.inspect_xml_tree(instructions_root)

        imported_list = []
        for child in root:
            # scan(child, 'root')
            part = create_object(Part.inspect_xml_tree(child), decoder_instructions)
            if not PartCatalog.check_presence(part):
                PartCatalog.add_part(part)
        print('catalog now has', len(PartCatalog.catalog))




