#-*- coding:utf8 -*-

import os
import sys
import re
import json


class ConfigHandler(object):

    def __init__(self, config_json_path=None):
        if config_json_path:
            self.config = json.load(open(config_json_path))
        else:
            self.config = dict()

    @property
    def image_formats(self):
        return self.config["image_formats"]

    @property
    def excluded_folders(self):
        return self.config["excluded_folders"]

    def excluded_files(self, path):
        return self._get_obj_from_path(path)["excluded_files"]

    def _get_obj_from_path(self, path):
        """Internal"""
        return self.config["paths"][path]

    def title(self, path):
        """
        returns the title to display when referring
        to the folder with the given path.
        paths should be like
        > "anime/yahari"
        > "games/ff14"
        """
        return self._get_obj_from_path(path)["title"]

    def physical_path(self, path):
        return self._get_obj_from_path(path)["fspath"]


def filterImages(files, cfg):
    """this function just filter images using given image formats."""
    regex = "\.(" + "|".join(cfg.image_formats) + ")$"
    #filter(lambda s: re.match(regex, s), files)
    return [s for s in files if re.findall(regex, s)]


def generateIndex(path, files, dirs):
    """
    this is the function that generates the HTML page
    that will be shown to the user
    """
    raise NotImplementedError("must add jinja2")


def goDeeper(starting_path, cfg):
    for root, dirs, files in os.walk(starting_path, topdown=True):
        files[:] = filterImages(files)
        #won't walk into some "excluded paths" (if needed)
        dirs[:] = [d for d in dirs if d not in cfg.excluded_folders]

        generateIndex(root, files, dirs)

if __name__ == "__main__":
    spath = sys.argv[1]
    try:
        cfgpath = sys.argv[2]
    except IndexError:
        cfgpath = './cfg.json'
    cfghandler = ConfigHandler(cfgpath)
    goDeeper(spath, cfghandler)
