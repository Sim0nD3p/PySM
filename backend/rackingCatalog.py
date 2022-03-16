
class StoreObjects:
    objects = []
    def __init__(self):
        print('init rackingCatalog')

    @classmethod
    def type_filter(cls, element_type):
        for object in cls.objects:
