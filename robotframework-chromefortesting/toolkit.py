import datetime
import hashlib
import os
import shutil
from zipfile import ZipFile, ZipInfo

from requests import Response

# Translate permissions across platforms
class PureZipFile(ZipFile):
    def _extract_member(self, member, path, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)
        path = super()._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        if attr != 0: os.chmod(path, attr)
        return path

# Process bytes from Response and extract zip
def process_extract_assets(version: str, channel_path: str, *_bytes: Response) -> None:
    zip_path = os.path.join(channel_path, f"chrome_{version}.zip")
    for bytes in _bytes:
        with open(zip_path, "wb") as file:
            file.write(bytes.content)
        with PureZipFile(zip_path, "r") as archive:
            archive.extractall(channel_path)
        os.remove(zip_path)

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

# Reset current Chrome for Testing installation
def reset_assets_location(path) -> None:
    if os.path.exists(path): 
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    [os.remove(os.path.join(path, file)) for file in os.listdir(path) if file.endswith('.zip')]

# Generate timestamp
def get_timestap() -> str:
    return str(datetime.datetime.now(datetime.timezone.utc))