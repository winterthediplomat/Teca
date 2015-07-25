from functools import reduce
import random
from string import ascii_letters, digits
import os
import teca.filesystem as tecafs
from six import next as _next
import logging

def _d(n, k):
    return reduce(lambda x, y: x*y, range(n-k+1, n+1), 1)

def generateToken(list_of_tokens=None, lenght=7, alphabet=ascii_letters+digits):
    if not list_of_tokens:
        list_of_tokens = dict()

    #anti endless loop math ahead!
    if len(list_of_tokens) == _d(len(alphabet), lenght):
      raise ValueError("it's not possible to generate a new token!")

    is_ok, new_token = False, None
    while not is_ok :
        new_token = "".join(random.sample(alphabet, lenght))
        is_ok = new_token not in list_of_tokens

    return new_token

def chooseImage(path, files, cfg):
    try:
        filename = random.choice(files)
    except IndexError:
        #there are no files, so we have to look to a file in a subfolder

        logging.debug("[choose_image] there are no images in {0}".format(path))

        try:
            lower_file_list = list(tecafs.walk(path, cfg, deep=True))[0]
            filename = random.choice(lower_file_list.filenames)
        except IndexError:
            filename = cfg.default_image
    #    try:
    #        chosen_dir = random.choice(dirs)
    #        try:
    #            logging.debug("[choose_image] the path we're looking files into: {0}".format(os.path.join(path, chosen_dir)))
    #            _, _, files = _next(tecafs.walk(os.path.join(path, chosen_dir)))
    #            filename = os.path.join(os.path.join(path, chosen_dir), random.choice(files))
    #        except IndexError:
    #            #there are directories, but no files. we should go deeper.
    #            filename = chooseImage(os.path.join(path, chosen_dir), files, cfg)
    #    except IndexError:
    #        #no files and no dirs... let's provide a default image.
    #        filename = cfg.default_image
    return filename

def chooseCoverImage(path, files, cfg):
    filename=cfg.cover_image_name(path) or chooseImage(os.path.join(cfg.starting_path, path), files, cfg)
    return os.path.join(path, filename)
