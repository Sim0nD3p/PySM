from elements.part.Part import Part

class PartCatalog:
    catalog = []


    @classmethod
    def get_part(cls, code: str):
        """

        :param code: code (string)
        :return: part
        """
        output = None
        for part in cls.catalog:
            if part.code == code:
                output = part
        return output

    @classmethod
    def filter_path(cls, source, property_path, search_value: str):
        """
        Searches the catalog for value in path
        :param source: source to look for search value
        :param property_path: list or string
        :param search_value: string value to search for
        :return:
        """
        if source is None:
            source = cls.catalog

        if search_value is None:
            return source

        results = []
        for part in source:
            if type(property_path) is str:
                value = part.get_path_property_value(property_path)
                if search_value.casefold() is not None and search_value.casefold() in str(value).casefold():
                    if part not in results:
                        results.append(part)
            elif type(property_path) is list:
                for path in property_path:
                    value = part.get_path_property_value(path)
                    if value is not None and search_value.casefold() in str(value).casefold():
                        if part not in results:
                            results.append(part)

        return results



    @classmethod
    def text_search(cls, source, text):
        """
        OLD
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
    def get_all_values_instance_for_property(cls, property_path):
        """
        Gets a list of values in PartCatalog for a given property path
        :param property_path:
        :return: list of values
        """
        existing_values = []
        for part in cls.catalog:
            value = part.get_path_property_value(property_path)
            if value not in existing_values and value is not None:
                existing_values.append(value)
        return existing_values



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

    @classmethod
    def remove_part(cls, part):
        """
        remove part in catalog (could be better to account for error)
        :param part: part object
        :return: void
        """

        if type(part) is str:
            if cls.get_part(part) is not None:
                cls.catalog.remove(cls.get_part(part))
        else:
            if part in cls.catalog:
                cls.catalog.remove(part)





