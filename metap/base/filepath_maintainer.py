import os

import meta


class FilePathMaintainer(object):
    def __init__(self):
        pass

    def get_package_absolute_directory(self, package):
        abs_dir_path = os.path.abspath(package.__file__)
        idx = abs_dir_path.rfind("/")
        abs_dir_path = abs_dir_path[:idx]
        return abs_dir_path

    def get_meta_package_absolute_directory(self):
        return self.get_package_absolute_directory(meta)

    def get_this_module_absolute_directory(self, module_magic_file: str):
        abs_dir_path = os.path.abspath(module_magic_file)
        idx = abs_dir_path.rfind("/")
        abs_dir_path = abs_dir_path[:idx]
        return abs_dir_path

    def get_evaluation_file_directory(self):
        project_path = self.get_package_absolute_directory()
        return project_path + "/evaluation/"

    def get_file_create_time(self, file_path: str):
        t = os.path.getctime(file_path)
        return t

    def get_file_directory(self, filepath: str) -> str:
        idx = filepath.rfind("/")
        return filepath[:idx]