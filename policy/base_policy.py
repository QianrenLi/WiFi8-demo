from abc import abstractmethod, ABC
from sedes.ap_list import AP_List

class BasePolicy(ABC):
    
    @abstractmethod
    def AP_selection(self, ap_list:AP_List):
        pass