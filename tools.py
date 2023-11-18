import hashlib
import os
from zipfile import ZipFile, ZipInfo

# Translate permissions across platforms
class PureUnzip(ZipFile):
    def _extract_member(self, member, path, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)
        path = super()._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        if attr != 0: os.chmod(path, attr)
        return path


# Validate binaries integrity 
def get_hash(path: str) -> str:

    def calc_hash(path: str) -> str:
        hash_func = hashlib.new("md5")
        with open(path, 'rb') as file:
            block = file.read(4096)
            while len(block) > 0:
                hash_func.update(block)
                block = file.read(4096)
        return hash_func.hexdigest()

    return "".join([calc_hash(os.path.join(root, file)) for root, _, files in os.walk(path) for file in files])


# Expose binaries to OS
def expose_binaries(*paths: str) -> str:
    for path in paths:
        os.environ['PATH'] = os.pathsep.join([os.path.abspath(path), os.environ.get('PATH', '')])
    return True


# Process output_path with backslash escape on Windows