from part.Part import Part

class PartCatalog:
    catalog = []

    def get_part(self, code):
        output = None
        for part in self.catalog:
            if part.code == code:
                output = part
        return output

    @classmethod
    def text_search(cls, source, text):
        """
        Search for string in all prop of part
        :param text: string
        :return: list of part object
        """
        results = []
        def check_part(current_part):
            part_content = Part.inspect_part_object(current_part)
            for prop in part_content:
                if type(part_content[prop]) == str:
                    if part_content[prop].find(text) != -1:
                        return current_part
            return None

        # not implemented yet, search in specific field
        def check_branch(branch):
            branch_content = Part.inspect_part_object(branch)

        if source is None:
            source = cls.catalog

        for part in source:
            if check_part(part) is not None:
                results.append(part)

        return results

    @classmethod
    def get_all_types(cls):
        """
        Gets all the parts types present in the catalog
        :return: list of types (string)
        """
        types = []
        for part in cls.catalog:
            if hasattr(part, 'general_information'):
                if hasattr(part.general_information, 'type'):
                    if part.general_information.type != 'error':
                        if part.general_information.type not in types:
                            types.append(part.general_information.type)

        # should add sort in alpabetical order
        print(type(types), types)

        return types

    @classmethod
    def get_catalog(cls):
        """
        Returns catalog
        :return: dict: catalog
        """
        return cls.catalog

    @classmethod
    def delete_catalog(cls):
        cls.catalog = []

    @classmethod
    def check_presence(cls, part):
        """
        Check if given part object is present in catalog
        :param part: part object
        :return: bool
        """
        if type(part) == str:
            for entry in cls.catalog:
                if entry.code == part:
                    return True
        else:
            for entry in cls.catalog:
                if entry.code == part.code:
                    return True

        return False


    @classmethod
    def print_catalog(cls):
        """
        prints catalog
        :return: void
        """
        print(cls.catalog)

    @classmethod
    def add_part(cls, part):
        """
        Add part to catalog (absolute)
        **error if part is already in catalog?
        :param part:
        :return:
        """
        cls.catalog.append(part)





