import random

from elements.store.storeObject import StoreObject

class StoreFloor:
    objects = []

    @classmethod
    def ids(cls):
        """
        :return: lsit of all ids of objects in storeFloor
        storeObject:
        as far as racking->shelf->storage_object
        """
        ids = []
        for obj in cls.objects:
            ids.append(obj.id)
            if hasattr(obj, 'shelves'):
                for shelf in obj.shelves:
                    ids.append(shelf.id)
                    for storage_group in shelf.storage_objects:
                        ids.append(storage_group.id)

        return ids

    @classmethod
    def generate_id(cls):
        """
        Generate a unique 6 digits numerical id
        :return: int
        """
        id = random.randrange(100000, 1000000, 1)
        if id not in cls.ids():
            cls.ids
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
        Searchs for shelves in all storeObject that have shelves
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

    @classmethod
    def get_id_object(cls, object_id: int):
        for object in cls.objects:      # looping thru storeObject
            if hasattr(object, 'shelves'):
                if object.id == object_id:
                    return object       # returning object
                for shelf in object.shelves:    # looping thru shelves
                    if shelf.id == object_id:
                        return shelf            # returning shelf
                    for storage_group in shelf.storage_objects:     # looping thru storage_group
                        if storage_group.id == object_id:
                            return storage_group                    # returning storage_group
        return None     # Not found


    @classmethod
    def delete_store_object(cls, object_id: int):
        """
        Search and deletes the object with the given id
        :param object_id: int
        :return: void
        """
        element = cls.get_id_object(object_id=object_id)
        if element not in cls.objects:
            for obj in cls.objects:
                if hasattr(obj, 'shelves'):
                    if element not in obj.shelves:
                        for shelf in obj.shelves:
                            if element not in shelf.storage_objects:
                                print('element not found, id:', element.id)
                            else:
                                shelf.storage_objects.remove(element)
                    else:
                        obj.shelves.remove(element)

        else:
            cls.objects.remove(element)






