import datetime
import hashlib
import os
import subprocess
from zipfile import ZipFile, ZipInfo

# Translate permissions across platforms
class ExtendedZipFile(ZipFile):
    def _extract_member(self, member, path, pwd) -> str:
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)
        path = super()._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        if attr != 0: os.chmod(path, attr)
        return path

# Validate binaries integrity 
def get_hash(path: str) -> str:

    def calculate_hash(path: str) -> str:
        hash_func = hashlib.new("md5")
        with open(path, 'rb') as file:
            block = file.read(4096)
            while len(block) > 0:
                hash_func.update(block)
                block = file.read(4096)
        return hash_func.hexdigest()

    return "".join([calculate_hash(os.path.join(root, file)) for root, _, files in os.walk(path) for file in files])

# Generate timestamp
def get_timestap() -> str:
    return str(datetime.datetime.now(datetime.timezone.utc))

# Permission setting
def set_permissions(platform, chrome_path, chromedriver_path) -> None:
    if "win" in platform:
        subprocess.run(['icacls', os.path.join(chrome_path, "chrome.exe"), '/grant', '*S-1-1-0:(RX)'])
        subprocess.run(['icacls', os.path.join(chromedriver_path, "chromedriver.exe"), '/grant', '*S-1-1-0:(RX)'])
    elif "mac" in platform:
        os.chmod(os.path.join(chrome_path, "Google Chrome for Testing.app"), 0o755)
        os.chmod(os.path.join(chromedriver_path, "chromedriver"), 0o755)
    else:
        os.chmod(os.path.join(chrome_path, "chrome"), 0o755)
        os.chmod(os.path.join(chromedriver_path, "chromedriver"), 0o755)
