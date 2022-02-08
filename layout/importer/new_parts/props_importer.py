from layout.importer.new_parts.part_importer import Importer
from backend.PartCatalog import PartCatalog
from part.Part import Part
from layout.importer.jsonImporter import JsonImporter
from layout.importer.xmlImporter import XmlImporter
from layout.importer.treeInspector import TreeInspector


class PropsImporter(Importer):
    def __init__(self):
        super().__init__()



    def get_part_from_instructions(self, instructions, data):
        """
        Gets part from catalog
        :param instructions:
        :param data:
        :return: part object
        """
        path = instructions['part/code']
        if data[path]:
            return PartCatalog.get_part(data[path])
        else:
            return None




    def import_props_to_part(self, instructions, data):
        """
        Add props to part:
        get part, with instructions add props
        :param instructions:
        :param data:
        :return:
        """
        part = self.get_part_from_instructions(instructions, data)
        part = Part.add_custom_prop(part, data, instructions)

        part_dict = Part.inspect_part_object(part)

        for object_path in instructions:
            object_dir = object_path.split('/')
            value = None
            if instructions[object_path] in data:
                value = Part.get_value(data, instructions, object_path)
            elif object_path in part_dict:
                value = part_dict[object_path]
            else:
                if object_path in instructions:
                    source_path = instructions[object_path]
                    if source_path in data:
                        value = data[source_path]

            part = Part.go_to_element(part, object_dir, value)



