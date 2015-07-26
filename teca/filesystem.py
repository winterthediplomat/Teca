import os
from six import next as _next
import re
import teca.utils as tecautils
from collections import namedtuple
import logging


Directory = namedtuple("Directory", "path directories filenames")

def walk(starting_path, cfg, deep=False):
    #print("teca.filesystem.walk: starting_path", starting_path)

    if not starting_path:
        starting_path = cfg.starting_path

    #print("teca.filesystem.walk: starting_path", starting_path)
    if not starting_path.startswith(cfg.starting_path):
        starting_path = os.path.join(cfg.starting_path, starting_path)

    #print("teca.filesystem.walk: starting_path", starting_path)
    at_least_one_folder = False

    deep_dirnames  = list()
    deep_filenames = list()

    for dirpath, dirnames, filenames in os.walk(starting_path):
        if isFolderHidden(dirpath, cfg, with_starting_path=True):
            break

        at_least_one_folder = True

        filterDirectories(dirpath, dirnames, cfg)
        filterFiles(dirpath, filenames, cfg)

        if not deep:
            yield dirpath, dirnames, filenames
        else:
            deep_dirnames.extend([os.path.join(dirpath, dirname_) for dirname_ in dirnames])
            deep_filenames.extend([os.path.join(dirpath, filename_) for filename_ in filenames])

    logging.debug("at_least_one_folder: {0}".format(at_least_one_folder))
    if not at_least_one_folder:
        yield Directory("", [], [])
    elif deep:
        yield Directory(starting_path, deep_dirnames, deep_filenames)



def filterDirectories(dirpath, dirnames, cfg):
    filterAccordingToFunction(dirpath, dirnames, cfg, cfg.excluded_folders)

def filterFiles(dirpath, fnames, cfg):
    #remove files if they're excluded
    filterAccordingToFunction(dirpath, fnames, cfg, cfg.excluded_files)
    #remove files if their extension is not supported
    fnames[:] = tecautils.filterImages(fnames, cfg)
    filterFilesIfInExcludedFileFormat(dirpath, fnames, cfg)

def filterFilesIfInExcludedFileFormat(dirpath, fnames, cfg):
    dirpath = dirpath.replace(cfg.starting_path, "")
    fnames[:] = [fname for fname in fnames if not cfg.excluded_file_formats(fname)]

def filterAccordingToFunction(dirpath, items, cfg, function_):
    dirpath = dirpath.replace(cfg.starting_path, "")
    for excluded in function_(dirpath):
        try:
            items.remove(excluded)
        except ValueError:
            pass


def filesInDirectory(dir_path, cfg, deep=False):
    _, _, fnames = _next(walk(dir_path, cfg, deep))
    return fnames

def isDirectoryEmpty(dir_path, cfg):
    _, dirnames, fnames = _next(walk(dir_path, cfg))
    return  (len(dirnames) + len(fnames)) == 0

def isFolderHidden(dir_path, cfg, with_starting_path=False):
    if with_starting_path:
        dir_path = dir_path.replace(cfg.starting_path, "")

    globally_excluded = dir_path in cfg.excluded_folders()
    locally_excluded  = os.path.basename(dir_path) in cfg.excluded_folders(os.path.dirname(dir_path))
    return globally_excluded or locally_excluded


# aliases
filesInFolder = filesInDirectory
