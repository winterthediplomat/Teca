import os
import six.next as _next
import re

def walk(starting_path, cfg):
    #raise NotImplementedError("walk")

    print("teca.filesystem.walk: starting_path", starting_path)

    if not starting_path:
        starting_path = cfg.starting_path

    print("teca.filesystem.walk: starting_path", starting_path)
    if not starting_path.startswith(cfg.starting_path):
        starting_path = os.path.join(cfg.starting_path, starting_path)

    print("teca.filesystem.walk: starting_path", starting_path)
    at_least_one_folder = False
    for dirpath, dirnames, filenames in os.walk(starting_path):
        at_least_one_folder = True

        filterDirectories(dirpath, dirnames, cfg)
        filterFiles(dirpath, filenames, cfg)

        yield dirpath, dirnames, filenames

    if not at_least_one_folder:
        yield ("", [], [])



def filterDirectories(dirpath, dirnames, cfg):
    filterAccordingToFunction(dirpath, dirnames, cfg, cfg.excluded_folders)

def filterFiles(dirpath, fnames, cfg):
    filterAccordingToFunction(dirpath, fnames, cfg, cfg.excluded_files)

def filterAccordingToFunction(dirpath, items, cfg, function_):
    dirpath = dirpath.replace(cfg.starting_path, "")
    print("teca.filesystem.filterAccordingToFunction", function_)
    print("teca.filesystem.filterAccordingToFunction for", dirpath, "->",  function_(dirpath))
    for excluded in function_(dirpath):
        try:
            items.remove(excluded)
        except ValueError:
            pass


def filesInDirectory(dir_path, cfg):
    print("teca.filesystem.filesInDirectory", walk)
    _, _, fnames = _next(walk(dir_path, cfg))
    return fnames

filesInFolder = filesInDirectory

def isDirectoryEmpty(dir_path, cfg):
    print("teca.filesystem.isDirectoryEmpty", walk)
    _, dirnames, fnames = _next(walk(dir_path, cfg))
    return  (len(dirnames) + len(fnames)) == 0
