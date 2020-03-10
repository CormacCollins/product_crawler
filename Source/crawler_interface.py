from abc import ABC, abstractmethod

"""
Forces any crawler instance to have the below functions
"""
class crawler_interface(ABC):

    @abstractmethod
    def get_product_info(self, prod_url):
        """
        Takes product link and returns dictionary of values
        """
        pass

