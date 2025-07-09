from policy.base_policy import BasePolicy
from sedes.ap_list import AP_List

class PowerGreedyPolicy(BasePolicy):
    def __init__(self):
        super().__init__()
        
    def AP_selection(self, ap_list: AP_List):
        ap_with_maximum_power = ap_list.aps.sort_values(by='signal')
        ap = ap_with_maximum_power.iloc[-1]
        return ap
        