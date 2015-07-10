from functools import reduce
import random
from string import ascii_letters, digits
import os

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
        #return None
        #looking into subfolders
#        if cfg.use_verbose:
#            print("[choose_image] there are no images in {0}".format(path))
        _, dirs, _ = os.walk(path).next() #getting the first-level directories
        try:
            chosen_dir = random.choice([unicode(d) for d in dirs if d not in cfg.excluded_folders(path)])
            try:
#                if cfg.use_verbose:
#                    print("[choose_image] the path we're looking files into: {0}".format(os.path.join(path, chosen_dir)))
                _, _, files = os.walk(os.path.join(path, chosen_dir)).next()
                files = [unicode(f) for f in filterImages(files, cfg)
                     if f not in cfg.excluded_files(chosen_dir)
                     and not cfg.excluded_file_formats(f)]
                filename = os.path.join(os.path.join(path, chosen_dir), random.choice(files))
            except IndexError:
                #there are directories, but no files. we should go deeper.
                filename = chooseImage(os.path.join(path, chosen_dir), files, cfg)
        except IndexError:
            #no files and no dirs... let's provide a default image.
            filename = cfg.default_image
    return filename

def chooseCoverImage(path, files, cfg):
    filename=cfg.cover_image_name(path) or chooseImage(os.path.join(cfg.starting_path, path), files, cfg)
    return os.path.join(path, filename)
