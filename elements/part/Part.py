from layout.settings.settings import Settings
from elements.part.dataClasses import GeneralInformation, Specifications
from elements.part.usage.orderHistory import OrderHistory
from elements.part.usage.usageDataClasses import Date
import xml.etree.ElementTree as et
"""
    **TF
    ----- NOMENCLATURE -----
    - SEPXXX-XXXXXX
    
    ----- GENERAL INFORMATION -----
    - type (3 premiers chiffres apres SEP), possible types vs type E21
    - niveau (piece, assemblage, option)
    - niveau piece
    
    
    
"""


def make_float(value):
    try:
        number = float(value)
        return number
    except ValueError:
        return 'NaN'


class Part:
    """
    essentials components of Part:
        - code
        - general information
        - technical information
        - specs
        - usage_stats
        - market (suppliers?)
        TODO: write getter methods to simplify
    """
    def __init__(self, code: str):
        self.code = code
        self.order_history = OrderHistory()
        self.general_information = None
        self.specifications = None
        self.order_stats = {
            'annual_average': None,
            'monthly_average': None,
            'average_order_frequency': None,
            'average_order_size': None,
            'order_number': None
        }

    def weight(self):
        """
        Weight of the part
        :return: float
        """
        if self.specifications and self.specifications.weight:
            try:
                return float(self.specifications.weight)
            except ValueError:
                return None
        else:
            return None

    def add_orders_to_history(self, orders):
        """
        Adds multiple orders to order_history and updates order_stats using self.add_order_to_history
        :param orders: order list
        :return: void
        """
        for order in orders:
            self.add_order_to_history(order)

    def add_order_to_history(self, order):
        """
        Adds order to order_history (order_history.orders) and updates order_stats
        :param order: order object
        :return: void
        """
        self.order_history.add_order(order)
        self.update_order_stats()

    def update_order_stats(self):
        start_date = Date(2017, 1, 1)
        self.order_stats = {
            'annual_average': self.order_history.annual_average(start_date.year),
            'monthly_average': self.order_history.monthly_average(start_date, 6, 'single'),
            'average_order_frequency': self.order_history.order_frequency(start_date.year),
            'average_order_size': self.order_history.average_order_size(start_date.year),
            'order_number': self.order_history.total_order(start_date.get_date())

        }

    def get_path_property_value(self, property_path):
        """
        Might not work for properties that are dict and not object
        returns the value associated with the property path
        :param property_path:
        :return:
        """
        def go_to_next_step(root, next_steps):
            if len(next_steps) > 1:
                # print(vars(root))
                # print('next_step', next_steps)
                if hasattr(root, next_steps[0]):
                    # print('yes')
                    # print(root.__getattribute__(next_steps[0]))
                    return go_to_next_step(root.__getattribute__(next_steps[0]), next_steps[1:])
                else:
                    if next_steps[0] in root:
                        return go_to_next_step(root[next_steps[0]], next_steps[1:])
                    else:
                        print('error in get_path_property_value->go_to_next_step')
                        return None
            else:
                if hasattr(root, next_steps[0]):
                    return root.__getattribute__(next_steps[0])

                elif next_steps[0] in root:
                    return root[next_steps[0]]
                else:
                    print('error in get_path_property_value')
                    print(root, next_steps)

        return go_to_next_step(self, property_path.split('/')[1:])

    @staticmethod
    def get_default_properties_list():
        """
        Dict of all child properties and their paths
        (property: property_path)
        :return: list
        """
        properties = []
        tree = et.ElementTree()
        tree.parse(Settings.part_model_path)
        for path in Part.inspect_xml_tree(tree.getroot()):
            properties.append(path)

        return properties



    @staticmethod
    def inspect_part_object(part):
        """
        DOC
        :param part:
        :return:
        """
        rec = {}

        def scan(obj, root):
            if hasattr(obj, '__dict__'):
                for child in vars(obj):
                    new_root = root + '/' + child
                    scan(vars(obj)[child], new_root)
            else:
                if type(obj) == dict or type(obj) == list:
                    for child in obj:
                        new_root = root + '/' + child
                        scan(obj[child], new_root)
                else:
                    rec[root] = obj

        scan(part, 'part')  # replace string by setting prop
        return rec

    @staticmethod
    def inspect_xml_tree(tree):
        """
        Returns the path of all child element and their text value in xml tree
        :param tree: xml.ElementTree.Element to return child properties
        :return: dict(path:value)
        """
        rec = {}

        def loop(branch, path):
            def get_path(root, p):
                if len(root) == 0:  # when element has no child, we return the element and its path
                    pa = path + '/' + root.tag
                    val = root.text
                    en = [pa, val]
                    return en
                else:   # if element has child, we loop trough them
                    p = p + '/' + root.tag
                    loop(root, p)
            for child in branch:    # for every element in the branch
                value = get_path(child, path)
                if value is not None:
                    rec[value[0]] = value[1]

        loop(tree, tree.tag)
        return rec

    @staticmethod
    def inspect_json_tree(tree, parent_tag):
        rec = {}

        def scan(current_tree, current_parent_tag):
            for child in current_tree:
                if len(current_parent_tag) > 0:
                    new_root = current_parent_tag + '/' + child
                else:
                    new_root = child

                if type(current_tree[child]) == dict:
                    scan(current_tree[child], new_root)
                else:
                    rec[new_root] = current_tree[child]
                    # print(new_root, obj[child])

        scan(tree, parent_tag)
        return rec




    @staticmethod
    def get_value(data, instruction, full_path):
        """
        Handles the retrieval of value with instructions and data
        Gets value with instruction and data. Finds the data path with instruction[full_path]
        and then the value with data[instruction[full_path]]
        :param data: dict: data {"data_path": "data"}
        :param instruction: dict: instructions {"object_path": "data_path"}
        :param full_path: "object path" to get in instructions
        :return:
        """
        if full_path in instruction:
            if instruction[full_path] in data:
                return data[instruction[full_path]]
            else:
                return 'error'
        else:
            return 'error'

    @staticmethod
    def get_code(data, instructions):
        """
        get parts code
        :param data:
        :param instructions:
        :return: str: code
        """
        path = {'code': 'part/code'}

        code = Part.get_value(data, instructions, path['code'])

        return code

    @staticmethod
    def make_general_information(data, instructions):
        """
        Takes data dictionary and instructions dictionary and returns GeneralInformation dataclass.
        The function go search the data with the path of the property found in the instructions dictionary
        :param data: dict of all properties(path):value
        :param instructions: dict of all properties(path):path
        :return: GeneralInformation dataClass
        """
        paths = {
            'description': 'part/general_information/description',
            'type': 'part/general_information/type'
        }
        description = Part.get_value(data, instructions, paths['description'])
        part_type = Part.get_value(data, instructions, paths['type'])

        return GeneralInformation(description=description, type=part_type)

    @staticmethod
    def make_specifications(data, instructions):
        """
        Takes data dictionary and instructions dictionary and returns specifications dataclass.
        The function go search the data with the path of the property found in the instructions dictionary
        :param data:
        :param instructions:
        :return: Specifications dataclass
        """
        paths = {  # This is the paths of specifications in partModel, where
            'length': 'part/specifications/length',
            'width': 'part/specifications/width',
            'height': 'part/specifications/height',
            'weight': 'part/specifications/weight'
        }
        length = make_float(Part.get_value(data, instructions, paths['length']))
        width = make_float(Part.get_value(data, instructions, paths['width']))
        height = make_float(Part.get_value(data, instructions, paths['height']))
        weight = make_float(Part.get_value(data, instructions, paths['weight']))

        return Specifications(length=length, width=width, height=height, weight=weight)

    @classmethod
    def make_order_history(cls, xml_order_history):
        """
        Makes order_history from xml element given containing all orders,
        creates Order object from xml elements:
        <order>
            <part_code>part_code</part_code>
            <date>yyyy-mm-dd</date>
            <quantity>quantity</quantity>
            <supplier>supplier</supplier>
        </order>


        :param xml_order_history: xml element of order as above
        :return: order_history
        """
        for child in xml_order_history:
            print(child)
        print('order history')


    @staticmethod
    def go_to_element(current_part, directions, current_value):
        """
        *might change name
        Go to path, assign value and returns part
        :param current_part: part object
        :param directions: directions of path split array ex: ['part', 'general_information', 'description']
        :param current_value: value for the property
        :return: part
        """
        placeholder = current_part
        # print('placeholder', placeholder)
        for i in range(len(directions)):  # for each direction in the path
            # print('path[i]', path[i])
            if i > 0:
                if hasattr(placeholder, '__dict__'):
                    if i == len(directions) - 1:
                        # print('path[i]: currentvalue', path[i], current_value)
                        placeholder.__setattr__(directions[i], current_value)
                        return current_part
                    else:
                        placeholder_child_value = {}
                        if hasattr(placeholder, directions[i]):
                            placeholder_child_value = placeholder.__getattribute__(directions[i])
                        placeholder.__setattr__(directions[i], placeholder_child_value)
                        placeholder = placeholder.__getattribute__(directions[i])
                else:
                    if i == len(directions) - 1:
                        placeholder[directions[i]] = current_value
                        return current_part
                    else:
                        if directions[i] not in placeholder:
                            placeholder[directions[i]] = {directions[i + 1]: 'something'}
                        placeholder = placeholder[directions[i]]

    @staticmethod
    def add_custom_prop(part, data, instructions):
        """
        add custom props to given path and return the part with properties added
        :param part: part object
        :param data: data in form of list of all properties: value
        :param instructions: instructions in form of list of all properties: properties path
        :return: part with added custom props
        """

        def get_value(object_path, instructions, data):
            if object_path in instructions:
                source_path = instructions[object_path]
                if source_path in data:
                    value = data[source_path]

        for object_path in instructions:    # go trough all the properties path of the partModel
            object_dir = object_path.split('/')     # split path in directions
            common_types = ['code', 'general_information', 'specifications', 'orders']
            if object_dir[1] not in common_types:   # excludes common types to only get custom properties
                value = None

                if object_path in instructions:   # if we have data with corresponding path given by instructions
                    # the instructions give {partModel path(object path): data path}
                    source_path = instructions[object_path]
                    if source_path in data:
                        value = data[source_path]

                part = Part.go_to_element(part, object_dir, value)

        return part


