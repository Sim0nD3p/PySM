from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()

    def draw_tree(self, part):
        self.clear()
        self.setColumnCount(2)
        self.setColumnWidth(0, 300)
        root = QTreeWidgetItem([part.code])
        self.addTopLevelItem(root)

        def get_element(object, root):
            if hasattr(object, '__dict__'):
                for child in vars(object):
                    child_content = object.__dict__[child]
                    child_element = QTreeWidgetItem([child])
                    root.addChild(child_element)
                    get_element(child_content, child_element)
            else:
                if type(object) == dict:
                    for child in object:
                        child_element = QTreeWidgetItem([child])
                        root.addChild(child_element)
                        child_content = object[child]
                        get_element(child_content, child_element)
                else:
                    if type(object) is None:
                        root.setText(1, 'none')
                    elif type(object) == str:
                        root.setText(1, object)
                    else:
                        root.setText(1, str(object))

        get_element(part, root)
        self.expandAll()


