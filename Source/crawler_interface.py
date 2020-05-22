from abc import ABC, abstractmethod

"""
Forces any crawler instance to adhere to simple requirement of taking
url link and returning information from it. 
Function can also have abilities to write to csv file with the provided path
"""
class crawler_interface(ABC):

    @abstractmethod
    def get_product_info(self, prod_url, store_name, path):
        """
        Takes product link and returns dictionary of values
        """
        pass

