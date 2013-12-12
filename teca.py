#-*- coding:utf8 -*-

import os
import re
import json
from optparse import OptionParser


class ConfigHandler(object):

    def __init__(self, config_json_path=None, options_from_cmd=None):
        if config_json_path:
            self.config = json.load(open(config_json_path))
        else:
            self.config = dict()
        if options_from_cmd:
            self.cmd_config = options_from_cmd
        else:
            self.cmd_config = dict()

    @property
    def use_verbose(self):
        return self.cmd_config["verbose"]

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

    def image_prefix_path(self, path):
        """
        fool idea: allowing links on other sites.
        it's transparent for the end user.
        """
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
    for actual_dir, dirs, files in os.walk(starting_path, topdown=True):
        if cfg.use_verbose:
            print(('walking into directory: ', actual_dir))
        files[:] = [f for f in filterImages(files)
                         if f not in cfg.excluded_files(actual_dir)]
        #won't walk into some "excluded paths" (if needed)
        dirs[:] = [d for d in dirs if d not in cfg.excluded_folders]
        if cfg.use_verbose:
            print('now generating index...')
        generateIndex(actual_dir, files, dirs)


def handleCmd():
    parser = OptionParser()
    parser.add_option('-c', '--config',
             dest='cfgpath',
             default='./cfg.json',
             help='the path of the configuration file'
        )
    parser.add_option('-v', '--verbose',
             default=False,
             help='useful for logging and debugging.'
        )
    (options, args) = parser.parse_args()
    return {
        "cfgpath": options.cfgpath,
        "verbose": options.verbose,
        "starting_path": args[0]
        }

if __name__ == "__main__":
    options = handleCmd()
    cfghandler = ConfigHandler(options['cfgpath'], options)
    goDeeper(options['starting_path'], cfghandler)