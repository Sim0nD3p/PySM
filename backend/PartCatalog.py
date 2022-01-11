
class PartCatalog:
    catalog = []

    def get_part(self, code):
        output = None
        for part in self.catalog:
            if part.code == code:
                output = part
        return output

    @classmethod
    def get_catalog(cls):
        return cls.catalog

    @classmethod
    def check_presence(cls, part):
        for entry in cls.catalog:
            if entry.code == part.code:
                return True
        return False


    @classmethod
    def print_catalog(cls):
        print(cls.catalog)

    @classmethod
    def add_part(cls, part):
        cls.catalog.append(part)

    @classmethod
    def get_catalog_data(cls, source_xml):
        """
        Called to populate the PartCatalog with parts in the backend/appData/catalog.xml file (the saved catalog)

        :param source_xml: source xml in appData
        :return: void
        """




