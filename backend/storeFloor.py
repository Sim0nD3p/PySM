from elements.store.storeObject import StoreObject

class StoreFloor:
    objects = []

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


