import os
from zipfile import ZipFile, ZipInfo

# Permissions translation across platforms
class extended_ZipFile(ZipFile):
    def _extract_member(self, member, path, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)
        path = super()._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        if attr != 0: os.chmod(path, attr)
        return path