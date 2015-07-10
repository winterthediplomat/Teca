#-*- coding:utf-8 -*-
import os
from optparse import OptionParser
import re

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
        "starting_path": os.path.abspath(args[0])
        }


def _next(iterator):
    try:
        print("teca.utils._next", iterator, dir(iterator))
        return next(iterator)
    except NameError:
        return iterator.next()

def filterImages(files, cfg):
    """this function just filter images using given image formats."""
    regex = "\.(" + "|".join(cfg.image_formats) + ")$"
    #filter(lambda s: re.match(regex, s), files)
    return [s for s in files if re.findall(regex, s)]
