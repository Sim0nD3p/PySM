
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

