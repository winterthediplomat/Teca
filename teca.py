# -*- coding: utf-8 -*-

#stdlib
import os
import re
import json
import random
from optparse import OptionParser
#external libraries
import jinja2

from teca.ConfigHandler import ConfigHandler
from teca.utils import handleCmd, filterImages

#fuckin' trick for UTF-8. That's the reason I flied away from Python a long time ago.
import sys
reload(sys) #adds setdefaultencoding in the available attributes
sys.setdefaultencoding('utf-8')

try:
    #let's try Pillow
    from PIL import Image
except ImportError:
    #not Pillow => you're using PIL
    import Image 


def generateCovers(path, files, cfg):
    def choose_image(path, files, cfg):
        try:
            filename = random.choice(files)
        except IndexError:
            #return None
            #looking into subfolders
            if cfg.use_verbose:
                print "[choose_image] there are no images in {0}".format(path)
            _, dirs, _ = os.walk(path).next() #getting the first-level directories
            try:
                chosen_dir = random.choice([unicode(d) for d in dirs if d not in cfg.excluded_folders(path)])
                try:
                    if cfg.use_verbose:
                        print "[choose_image] the path we're looking files into: {0}".format(os.path.join(path, chosen_dir))
                    _, _, files = os.walk(os.path.join(path, chosen_dir)).next()
                    files = [unicode(f) for f in filterImages(files, cfg)
                         if f not in cfg.excluded_files(chosen_dir)
                         and not cfg.excluded_file_formats(f)]
                    filename = os.path.join(os.path.join(path, chosen_dir), random.choice(files))
                except IndexError:
                    #there are directories, but no files. we should go deeper.
                    filename = choose_image(os.path.join(path, chosen_dir), files, cfg)
            except IndexError:
                #no files and no dirs... let's provide a default image.
                filename = cfg.default_image
        return filename
        
    filename=cfg.cover_image_name(path)
    if filename == ":random":
        #filename = choose_image(path, files, cfg)
        filename = choose_image(os.path.join(cfg.starting_path, path), files, cfg)
    full_filename = os.path.join(path, filename)
    try:
        cover_obj = Image.open(full_filename)
    except IOError:
        #TODO: probably it could fail if launching Teca from another folder
        if cfg.use_verbose:
            print "image {0} not found, looking {1}".format(full_filename, os.path.join(os.path.abspath(""), filename))
        cover_obj = Image.open(os.path.join(os.path.abspath(""), filename))
    cover_obj.thumbnail(cfg.cover_size(path))
    cover_obj.save(os.path.join(path, "cover_.png"))#+os.path.splitext(filename)[-1]))


def generateThumbnails(path, files, cfg):
    for filename in files:
        full_filename = os.path.join(path, filename)
        if not cfg.regenerate_thumbnails and os.path.exists(os.path.join(path, "thumb_"+filename)):
            if cfg.use_verbose:
                print("not generated the thumbnail for %s"%full_filename)
            continue
        if cfg.use_verbose:
            print("generating thumbnail for %s"%full_filename)
        try:
            thumbnail_obj = Image.open(full_filename)
            thumbnail_obj.thumbnail(cfg.thumbnail_size(path))
            thumbnail_obj.save(os.path.join(path, "thumb_"+filename))
        except:
            print("[ERROR][Thumbnails]: error while generating thumbnail for %s"%full_filename)


def generateIndex(path, files, dirs, cfg):
    """
    this is the function that generates the HTML page
    that will be shown to the user
    """
    if cfg.use_verbose:
        print("directories: "+"\n\t".join(dirs))
        print("files: "+"\n\tinserted: ".join(files))
        print("{0} -> >{1}< {2}".format(path, cfg.template_path(path), cfg.config.config["template_path"]))

    import codecs    
    codecs.open(os.path.join(path, "index.html"), "w", encoding = 'utf-8').write(
            jinja2.Template(
            open(cfg.template_path(path)).read()
                ).render(
                title = cfg.title(path),
                files = files,
                dirs = dirs,
                path = path,
                back_folder = not path and "" or "..",
                dirs_no = cfg.directories_on_a_row,
                images_no = cfg.images_on_a_row
            )
        )

def goDeeper(starting_path, cfg):
    for actual_dir, dirs, files in os.walk(starting_path, topdown=True):
        actual_dir = actual_dir #unicode_it(actual_dir, "utf8")
        if cfg.use_verbose:
            print(('walking into directory: ', actual_dir))
        
        files[:] = [unicode(f) for f in filterImages(files, cfg)
                         if f not in cfg.excluded_files(actual_dir)
                         and not cfg.excluded_file_formats(f)]
        #won't walk into some "excluded paths" (if needed)
        dirs[:] = [unicode(d) for d in dirs if d not in cfg.excluded_folders(actual_dir)]
        if cfg.use_verbose:
            print('now generating index...')
        generateCovers(actual_dir, files, cfg)
        generateThumbnails(actual_dir, files, cfg)
        generateIndex(actual_dir, files, dirs, cfg)


if __name__ == "__main__":
    options = handleCmd()
    cfghandler = ConfigHandler(options['cfgpath'], options)
    goDeeper(options['starting_path'], cfghandler)
