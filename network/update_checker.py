import requests
import json
from config import config

class UpdateChecker:
    def __init__(self):
        self.update_url = config.UPDATE_SERVER
        self.current_version = config.GAME_VERSION
    
    def check_for_updates(self):
        try:
            response = requests.get(self.update_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('tag_name', self.current_version)
                return latest_version, self.compare_versions(latest_version, self.current_version) > 0
        except:
            pass
        return self.current_version, False
    
    def compare_versions(self, v1, v2):
        try:
            parts1 = [int(x) for x in v1.replace('v', '').split('.')]
            parts2 = [int(x) for x in v2.replace('v', '').split('.')]
            for i in range(max(len(parts1), len(parts2))):
                a = parts1[i] if i < len(parts1) else 0
                b = parts2[i] if i < len(parts2) else 0
                if a > b:
                    return 1
                if a < b:
                    return -1
            return 0
        except:
            return 0