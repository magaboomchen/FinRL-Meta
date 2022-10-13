import json
import os
from typing import List

from meta.local.base.filepath_maintainer import FilePathMaintainer


class SettingLoader(object):
    def __init__(self):
        pass

    def load_json(self, filepath: str) -> List:
        with open(filepath, "r") as f:
            return json.load(f)

    @classmethod
    def load_tushare_setting(cls):
        loader_dir = FilePathMaintainer().get_this_module_absolute_directory(__file__)
        tushare_setting_filepath = os.path.join(loader_dir, "token.json")
        return cls.load_json(cls, tushare_setting_filepath)
