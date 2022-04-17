from elements.container.bin import Bin

bin1 = Bin(name='test1', length=200, width=100, height=50)


class ContainerCatalog:
    containers = [bin1]

    @classmethod
    def get_containers(cls, container_type):
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
