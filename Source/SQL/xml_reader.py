import xml.etree.ElementTree as ET
'''
Helper class for extracting easy table attributes from xml file
'''

class reader():

    def __init__(self, path):
        '''
        Initialize reader with root and tree accessible
        '''
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.table_names = self.get_root_children_names(self.root)

    
    def get_text_contents_children(self, parent_name):
        '''
        Get the text inside the xml tags of children of the supplied tag
        '''
        children_text = list()
        for tbl in self.root.findall(parent_name):
            for col in tbl:
                children_text.append(col.text)
        return children_text

    def get_children_names_of_parent(self, parent_name):
        '''
        Get the names of children tags of the parent
        '''
        children_names = list()
        for tbl in self.root.findall(parent_name):
            for col in tbl:
                children_names.append(col.tag)
        return children_names

    def get_root_children_names(self, root):
        tables = list()
        for tbl in root:
            tables.append(tbl.tag)
        return tables