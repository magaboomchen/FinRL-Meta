#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import site
import subprocess


class EnvironmentSetter(object):
    def __init__(self):
        pass

    def addPythonModule2SystemPath(self,path, pthfileName="finrlmeta.pth"):
        directorys = site.getsitepackages()
        for direct in directorys:
            try:
                shellCmd = "sudo sh -c 'echo  " + path + " > " \
                    + direct + "/" + pthfileName + "'"
                subprocess.check_output([shellCmd], shell=True)
            except:
                pass


if __name__=="__main__":
    eS = EnvironmentSetter()
    thisModuleAbsPath = os.path.abspath(__file__)
    thisModuleAbsPath = thisModuleAbsPath.replace("/local/base/package_path_setter.py"," ")
    eS.addPythonModule2SystemPath(thisModuleAbsPath)