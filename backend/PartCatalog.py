
class PartCatalog:
    catalog = []

    def get_part(self, code):
        output = None
        for part in self.catalog:
            if part.code == code:
                output = part
        return output

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




