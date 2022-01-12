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
    def text_search(cls, text):
        print('searching string', text)

        results = []

        def check_part(current_part):
            part_content = Part.inspect_part_object(current_part)
            for prop in part_content:
                if type(part_content[prop]) == str:
                    if part_content[prop].find(text) != -1:
                        return current_part
            return None

        for part in cls.catalog:
            if check_part(part) is not None:
                results.append(part)

        return results



    @classmethod
    def get_catalog(cls):
        """
        Returns catalog
        :return: dict: catalog
        """
        return cls.catalog

    @classmethod
    def check_presence(cls, part):
        """
        Check if given part object is present in catalog
        :param part: part object
        :return: bool
        """
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





