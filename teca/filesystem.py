import os
from six import next as _next
import re
import teca.utils as tecautils

def walk(starting_path, cfg):
    #raise NotImplementedError("walk")

    #print("teca.filesystem.walk: starting_path", starting_path)

    if not starting_path:
        starting_path = cfg.starting_path

    #print("teca.filesystem.walk: starting_path", starting_path)
    if not starting_path.startswith(cfg.starting_path):
        starting_path = os.path.join(cfg.starting_path, starting_path)

    #print("teca.filesystem.walk: starting_path", starting_path)
    at_least_one_folder = False

    for dirpath, dirnames, filenames in os.walk(starting_path):
        if isFolderHidden(dirpath, cfg, with_starting_path=True):
            break

        at_least_one_folder = True

        filterDirectories(dirpath, dirnames, cfg)
        filterFiles(dirpath, filenames, cfg)

        yield dirpath, dirnames, filenames

    if not at_least_one_folder:
        yield ("", [], [])



def filterDirectories(dirpath, dirnames, cfg):
    filterAccordingToFunction(dirpath, dirnames, cfg, cfg.excluded_folders)

def filterFiles(dirpath, fnames, cfg):
    #remove files if they're excluded
    filterAccordingToFunction(dirpath, fnames, cfg, cfg.excluded_files)
    #remove files if their extension is not supported
    fnames[:] = tecautils.filterImages(fnames, cfg)

def filterAccordingToFunction(dirpath, items, cfg, function_):
    dirpath = dirpath.replace(cfg.starting_path, "")
    for excluded in function_(dirpath):
        try:
            items.remove(excluded)
        except ValueError:
            pass


def filesInDirectory(dir_path, cfg):
    _, _, fnames = _next(walk(dir_path, cfg))
    return fnames

filesInFolder = filesInDirectory

def isDirectoryEmpty(dir_path, cfg):
    _, dirnames, fnames = _next(walk(dir_path, cfg))
    return  (len(dirnames) + len(fnames)) == 0

def isFolderHidden(dir_path, cfg, with_starting_path=False):
    if with_starting_path:
        dir_path = dir_path.replace(cfg.starting_path, "")

    globally_excluded = dir_path in cfg.excluded_folders()
    locally_excluded  = os.path.basename(dir_path) in cfg.excluded_folders(os.path.dirname(dir_path))
    return globally_excluded or locally_excluded

