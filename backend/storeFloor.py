import random

from elements.store.storeObject import StoreObject

class StoreFloor:
    objects = []

    @classmethod
    def ids(cls):
        """
        :return: lsit of all ids of objects in storeFloor
        """
        ids = []
        for obj in cls.objects:
            ids.append(obj.id)
        return ids

    @classmethod
    def generate_id(cls):
        """
        Generate a unique 6 digits numerical id
        :return: int
        """
        id = random.randrange(100000, 1000000, 1)
        if id not in cls.ids():
            return id
        else:
            cls.generate_id()

    @classmethod
    def get_floor_object_by_id(cls, id):
        """
        Gets the object that matches the given id
        :param id: int
        :return: floorObject
        """
        match = None
        for obj in cls.objects:
            if obj.id == id:
                match = obj
        return match

    @classmethod
    def get_shelf_by_id(cls, id):
        """
        Searchs all shelves to match given id
        :param id:
        :return:
        """
        match = None
        for obj in cls.objects:
            if hasattr(obj, 'shelves'):
                for shelf in obj.shelves:
                    if shelf.id == id:
                        match = shelf
        return match


    @classmethod
    def check_presence(cls, store_object: StoreObject):
        """
        Checks if the given object is in store floor
        :param store_object: storeObject
        :return: Bool
        """
        if store_object in cls.objects:
            return True
        else:
            return False

    @classmethod
    def add_object(cls, store_object: StoreObject):
        """
        Adds object to store floor
        :param store_object: storeObject
        :return: void
        """
        if not cls.check_presence(store_object=store_object):
            cls.objects.append(store_object)
        else:
            print('object already in store floor')

        # print('object added to floor', cls.objects)


