from part.dataClasses import GeneralInformation, Specifications
"""
    ESSENTIALS ATTRIBUTES FOR PARTS
    -code
    -description
    -use_case
    
    
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

    @staticmethod
    def inspect_tree(tree):
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
    def get_code(data, instructions):
        """
        get parts code
        :param data:
        :param instructions:
        :return: str: code
        """
        path = {'code': 'part/code'}

        code = data[instructions[path['code']]]

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
            'description': 'part/general_information/description'
        }
        description = data[instructions[paths['description']]]

        return GeneralInformation(description=description)

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
        length = data[instructions[paths['length']]]
        width = data[instructions[paths['width']]]
        height = data[instructions[paths['height']]]
        weight = data[instructions[paths['weight']]]

        return Specifications(length=length, width=width, height=height, weight=weight)

    @staticmethod
    def add_custom_prop(part, data, instructions):
        """
        add custom props to given path and return the part with properties added
        :param part: part object
        :param data: data in form of list of all properties: value
        :param instructions: instructions in form of list of all properties: properties path
        :return: part with added custom props
        """
        for object_path in instructions:            # go trough all the properties path of the partModel
            object_dir = object_path.split('/')     # split path directions
            common_types = ['code', 'general_information', 'specifications']
            if object_dir[1] not in common_types:   # excludes common types to only get custom properties
                value = None
                if instructions[object_path] in data:   # if we have data with corresponding path given by instructions
                    # the instructions give {partModel path(object path): data path}
                    source_path = instructions[object_path]
                    value = data[source_path]

                def go_to_element(current_part, path, current_value):
                    placeholder = current_part
                    for i in range(len(path)):
                        if i > 0:
                            if hasattr(placeholder, '__dict__'):
                                if i == len(path) - 1:
                                    placeholder.__setattr__(path[i], current_value)
                                else:
                                    placeholder_child_value = {}
                                    if hasattr(placeholder, path[i]):
                                        placeholder_child_value = placeholder.__getattribute__(path[i])
                                    placeholder.__setattr__(path[i], placeholder_child_value)
                                    placeholder = placeholder.__getattribute__(path[i])
                            else:
                                if i == len(path) - 1:
                                    placeholder[path[i]] = current_value
                                    return current_part
                                else:
                                    if path[i] not in placeholder:
                                        placeholder[path[i]] = {path[i + 1]: 'something'}
                                    placeholder = placeholder[path[i]]

                part = go_to_element(part, object_dir, value)
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


