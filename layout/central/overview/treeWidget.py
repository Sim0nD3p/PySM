from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()

    def draw_tree(self, part):
        self.clear()
        self.setColumnCount(2)
        self.setColumnWidth(0, 300)
        # print(part)
        # print(part.__dict__)
        # print(part.code)
        root = QTreeWidgetItem([part.code])
        # print(root)
        self.addTopLevelItem(root)

        def get_element(object, root):
            # print('get_element, object:', object, 'root:', root)
            if hasattr(object, '__dict__'):
                # print('has __dict__')
                # print(vars(object))
                for child in vars(object):
                    # print(child)
                    # print('content', object.__dict__[child])
                    child_content = object.__dict__[child]
                    child_element = QTreeWidgetItem([child])
                    root.addChild(child_element)
                    get_element(child_content, child_element)
            else:
                # print('no __dict__, object:', object, type(object), type(object) == dict)
                if type(object) == dict:
                    # print('object is', object)
                    for child in object:
                        # print('child', child)
                        child_element = QTreeWidgetItem([child])
                        root.addChild(child_element)
                        child_content = object[child]
                        get_element(child_content, child_element)
                        # print('child_content:', child_content)
                else:
                    if type(object) is None:
                        root.setText(1, 'none')
                    elif type(object) == str:
                        root.setText(1, object)
                    else:
                        root.setText(1, str(object))

        get_element(part, root)
        self.expandAll()


