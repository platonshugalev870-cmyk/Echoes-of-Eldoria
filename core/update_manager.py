import requests
import json
import os
import zipfile
import shutil
from datetime import datetime

class UpdateManager:
    def __init__(self, current_version, update_url):
        self.current_version = current_version
        self.update_url = update_url
        self.update_available = False
        self.latest_version = current_version
        self.update_info = {}
    
    def check_for_updates(self):
        try:
            response = requests.get(self.update_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.latest_version = data.get('tag_name', self.current_version)
                if self.compare_versions(self.latest_version, self.current_version) > 0:
                    self.update_available = True
                    self.update_info = data
                    return True
        except Exception:
            pass
        return False
    
    def compare_versions(self, v1, v2):
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
    
    def download_update(self, callback=None):
        if not self.update_available:
            return False
        try:
            assets = self.update_info.get('assets', [])
            if assets:
                download_url = assets[0].get('browser_download_url')
                if download_url:
                    response = requests.get(download_url, stream=True)
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    update_path = 'update.zip'
                    with open(update_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                            downloaded += len(chunk)
                            if callback:
                                progress = (downloaded / total_size) * 100 if total_size > 0 else 0
                                callback(progress)
                    self.apply_update(update_path)
                    return True
        except Exception:
            return False
        return False
    
    def apply_update(self, zip_path):
        backup_dir = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        os.makedirs(backup_dir, exist_ok=True)
        for file in os.listdir('.'):
            if file.endswith('.py') or file.endswith('.json') or file.endswith('.txt'):
                shutil.copy2(file, os.path.join(backup_dir, file))
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')
        os.remove(zip_path)
        with open('version.txt', 'w') as f:
            f.write(self.latest_version)

update_manager = UpdateManager('2.0.0', 'https://api.github.com/repos/user/dungeon-crawler/releases/latest')