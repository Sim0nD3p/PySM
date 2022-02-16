from part.dataClasses import GeneralInformation, Specifications
from part.usage.orderHistory import OrderHistory
from part.usage.usageDataClasses import Date, Order
"""
    **TF
    ----- NOMENCLATURE -----
    - SEPXXX-XXXXXX
    
    ----- GENERAL INFORMATION -----
    - type (3 premiers chiffres apres SEP), possible types vs type E21
    - niveau (piece, assemblage, option)
    - niveau piece
    
    
    
"""

class Part:
    """
    essentials components of Part:
        - code
        - general information
        - technical information
        - specs
        - usage_stats
        - market (suppliers?)

    """
    def __init__(self, code: str):
        self.code = code
        self.order_history = OrderHistory()
        self.order_stats = {}

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
            'average_order_size': self.order_history.average_order_size(start_date.year)

        }



    @classmethod
    def inspect_part_object(cls, part):
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

        scan(part, 'part')
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
        length = Part.get_value(data, instructions, paths['length'])
        width = Part.get_value(data, instructions, paths['width'])
        height = Part.get_value(data, instructions, paths['height'])
        weight = Part.get_value(data, instructions, paths['weight'])

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

    @classmethod
    def make_part_from_instructions(cls, instructions, data):
        """
        :param instructions:
        :param data:
        :return:
        """


def target(xml_root, obj):


    def loop(xml_branch, obj_branch):

        for child in xml_branch:    # for each element of the xml branch
            print('looping ', xml_branch, ' --> ', child)   # parent --> child
            if hasattr(obj_branch, '__dict__'):             # object branch is a structure and has __dict__ attribute
                if child.tag in vars(obj_branch):           # the current xml child is in the object branch
                    print(child.tag, ' in ', obj_branch)
                    if len(child) > 0:                      # child inside a child
                        # xml_branch is child
                        # obj branch is vars(obj)[child.tag]
                        obj_child_prop = obj_branch.__getattribute__(child.tag)     # getting the object child propriety
                        print('000', vars(obj_branch))
                        o_b, o_b_tag = loop(child, obj_child_prop)          # getting the content for the propriety
                        obj_branch.__setattr__(o_b_tag, o_b)                # setting attribute for the object's branch
                        print(vars(obj_branch))
                        print(vars(obj_branch.specs))
                    else:                               # the attribute is already matching between xml and object
                        #print(obj_branch.__getattribute__(child.tag))
                        print(child.tag, '(xml) is ', vars(obj_branch)[child.tag], '(obj)')

                else:   # the attribute is present in xml but not in object
                    print(child.tag, ' not in ', vars(obj_branch))
                    print('xml_branch', xml_branch.tag)
                    print(type(obj_branch), child.tag)
                    obj_branch.__setattr__(child.tag, {})   # creating attribute at branch level in object

                    if len(child) > 0:  # if the current xml child also have child, we need to loop through them
                        o_b, o_b_tag = loop(child, obj_branch.__getattribute__(child.tag))      # getting content
                        obj_branch.__setattr__(o_b_tag, o_b)    # setting attribute on branch level in object

            else:   # base object is not a structure, dictionary is used instead so syntax differ a bit
                print(child)
                if len(child) > 0:
                    print(obj_branch)
                    print(child.tag)
                    o_b, o_b_tag = loop(child, {})
                    print(o_b, o_b_tag)
                    obj_branch[o_b_tag] = o_b

                else:
                    obj_branch[child.tag] = 'bon matin'

        print(xml_branch.tag)
        # print(vars(obj_branch))
        return [obj_branch, xml_branch.tag]

    output = loop(xml_root, obj)
    return output[0]




def scan_xml(xml_root, outstring):
    for child in xml_root:
        if len(child) == 0:
            print(outstring + '/' + child.tag)
        else:
            outstring = outstring + '/' + child.tag
            scan_xml(child, outstring)

def scan_obj(obj, target):
    if target not in vars(obj):
        # print(target, ' not in ', vars(obj))
        for child in vars(obj).items():
            # print('chcking type of child[1]', child)
            if hasattr(child[1], '__dict__'):
                # print(child[1], ' is ', type(child[1]))
                scan_obj(child[1], target)
    else:
        # print('found ', target, ' in ', vars(obj))
        return 'found'



'''
we want:
if xmlProp not in obj attr, add it at the good place
'''
# scan_xml(root, 'Part')
# f = scan_obj(e, 'class')
# print(hasattr(e, '__dict__'))


