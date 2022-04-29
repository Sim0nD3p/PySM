from elements.container.bin import *
from elements.container.spaceContainer import *
from elements.container.containerStack import *

bin1 = Bin(name='test1', length=200, width=100, height=50)
bin2 = Bin(name='Big bin', length=500, width=200, height=75)


class ContainerCatalog:
    containers = [bin1, bin2]

    @classmethod
    def get_containers(cls, container_type: type):
        """
        Return all containers with the given container type
        :param container_type:
        :return:
        """
        containers = []
        for container in cls.containers:
            if type(container) == container_type:
                containers.append(container)

        return containers

    @classmethod
    def custom_container(cls):
        pass

    @classmethod
    def create_containers_from_type(cls, container_type: Container, number: int):
        """
        Creates new containers from type in container class properties, return them in array
        :param container_type: the type of the container class ex.: SpaceContainer, Bin (not initialized)
        :param number: number of container to create
        :return:
        """
        containers = []
        for i in range(0, number):
            if container_type.type == SPACE_CONTAINER:
                containers.append(SpaceContainer('name' + str(i), 0, 0, 0))
            elif container_type.type == BIN:
                pass

        return containers


    @classmethod
    def create_containers(cls, container_instance: Container, number: int):
        print(container_instance)
        containers = []
        for i in range(0, number):
            if container_instance.type == BIN:
                e = Bin('name' + str(i), container_instance.length(), container_instance.width(),
                        container_instance.height())
                containers.append(e)
            elif container_instance.type == SPACE_CONTAINER:
                e = SpaceContainer('name' + str(i), container_instance.length(), container_instance.width(),
                                   container_instance.height())
                containers.append(e)
            else:
                containers.append(None)
        return containers



    @classmethod
    def create_containers_old(cls, class_type: type, number: int, options: dict):
        """
        Might be replaced with method that initialize container with special constructor
        returns empty containers
        :param class_type: instance of object
        :param number
        :param options: Container options for name and dimensions
        :return: list of empty containers
        """
        containers = []
        for i in range(0, number):
            if issubclass(type(class_type), Bin):
                c = Bin(name=options['name'], length=options['length'], width=options['width'], height=options['height'])
                containers.append(c)
            elif issubclass(type(class_type), SpaceContainer):
                c = SpaceContainer(name=options['name'], length=options['length'],
                                   width=options['width'], height=options['height'])
                containers.append(c)

        return containers



