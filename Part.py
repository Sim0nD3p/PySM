from dataclasses import dataclass
import xml.etree.ElementTree as et


@dataclass
class Specs:
    length: float
    width: float
    height: float
    weight: float


@dataclass
class DataContainer:
    h: any

@dataclass
class Ski:
    a: float
    b: str

@dataclass
class Container:
    dimensions: float
    type: Ski
"""
    ESSENTIALS ATTRIBUTES FOR PARTS
    -code
    -description
    -use_case
    
    
"""

class Part:
    def __init__(self, code, specs, container):
        self.code = code
        self.specs = specs
        self.cont = container


    #def __setattr__(self, key, value):
        # print('__setattr__')

    # def __setitem__(self, key, value):
      #   print('__setitem__')


    @classmethod
    def set_custom_attributes(cls):
        cla = cls('fdsf', 'fsdfs', 'fsd')
        cla.newrpor = 'test'
        return cla


xml_tree = et.ElementTree()
xml_tree.parse('partModel.xml')


sk = Ski(91, 'SIMON')
ct = Container(69, sk)
sp = Specs(10, 10, 10, 5)
e = Part('Simon', sp, ct)
r = Part.set_custom_attributes()


root = xml_tree.getroot()
# listProp = e.__dict__


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

new = target(root, e)
print(vars(new))
print(vars(new.specs))


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


