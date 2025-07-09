import re
import pandas as pd

class AP_List():
    def __init__(self, aps: pd.DataFrame):
        self.aps = aps
        pass
    
    
    @staticmethod
    def _parse_terminal(terminal_res:str):
        # Find all matches (handles multiple BSS blocks)
        pattern = r'''
                BSS\s+((?:[0-9a-f]{2}:){5}[0-9a-f]{2})  # MAC address (hex groups with colons)
                .*?                                      # Any characters (non-greedy)
                ^\s*freq:\s*(\d+)                        # Frequency (digits after 'freq:')
                .*?                                      
                ^\s*signal:\s*([-\d.]+)                  # Signal (numeric with -/decimal)
                .*?                                      
                ^\s*last\s+seen:\s*(\d+)\s*ms\s+ago      # Last seen (digits before 'ms ago')
                .*?                                      
                ^\s*SSID: (.*?)                        # SSID (any characters until newline)
                (?=\n\s*\S|\n\t|\Z)                         # Lookahead for next non-space/newline
                '''
        # Find all matches
        matches = re.finditer(pattern, terminal_res, flags=re.DOTALL | re.MULTILINE | re.VERBOSE | re.IGNORECASE)

        data = []
        for match in matches:
            # Strip whitespace from SSID and handle empty values
            ssid = match.group(5).strip()
            if not ssid:
                ssid = None  # Or use empty string ''
            
            data.append({
                'mac address': match.group(1),
                'freq': int(match.group(2)),
                'signal': float(match.group(3)),
                'last seen': int(match.group(4)),
                'ssid': ssid
            })

        # Create DataFrame
        df = pd.DataFrame(data)

        return df
    
    def if_ap_exist(self, mac_address):
        if mac_address in self.aps['mac address']:
            return True
        return False
    
    
    @staticmethod
    def from_terminal(terminal_res:str):
        return AP_List( AP_List._parse_terminal(terminal_res) )


    def update(self, terminal_res: str):
        new_df = AP_List._parse_terminal(terminal_res)
        
        ##TODO: mark the disappear and appear AP apart
        self.aps = new_df
        return self
        
    def __str__(self):
        return self.aps.to_string()