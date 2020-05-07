
#--------------- PRODUCTS FACT TABLE -------------------------------
import xml.etree.ElementTree as ET
#get all types and all measurements



class reader():

    def __init__(self, path):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.table_names = self.get_root_children_names()

    
    def get_text_contents_children(self, parent_name):
        children_text = list()
        for tbl in self.root.findall(parent_name):
            for col in tbl:
                children_text.append(col.text)
        return children_text


    def get_root_children_names(self):
        tables = list()
        for tbl in self.root:
            tables.append(tbl.tag)
        return tables