#-*- coding: utf-8 -*-
from __future__ import unicode_literals

#stdlib
import os
import re
import json
import random
from optparse import OptionParser
from string import ascii_letters
#external libraries
import jinja2

import teca
from teca.image import Image
from teca.ConfigHandler import ConfigHandler
from teca.utils import handleCmd, filterImages
import teca.generation
import teca.filesystem
import logging
logging.basicConfig(format="%(levelname)s:%(funcName)s->%(lineno)d:%(message)s", filemode="w", filename=".teca.log", level=logging.DEBUG)

#fuckin' trick for UTF-8. That's the reason I ran away from Python a long time ago.
#import sys
#reload(sys) #adds setdefaultencoding in the available attributes
#sys.setdefaultencoding('utf-8')

def generateShortLinks(path, dirs, files, cfg):
    token = teca.generation.generateToken
    
    if cfg.is_plugin_enabled("short_links"): #cfg.short_links.use_feature:
      
      with open(cfg.short_links.links_database) as links_file:
          links = json.load(links_file)
          for file_ in files:
              fullpath = os.path.join(path, file_)
              if fullpath not in links:
                  code = token(links.values())
                  os.symlink(os.path.join(cfg.short_links.symlink_folder, code), fullpath)
                  links[fullpath] = code
              else: #fullpath in links
                  if not os.path.exists(os.path.join(cfg.short_links.symlink_folder, links[fullpath])): #we need to recreate the token
                    os.symlink(os.path.join(cfg.short_links.symlink_folder, links[fullpath]))
      json.dump(links, open(cfg.short_links.links_database, "w"))

def generateCovers(path, files, cfg):
    choose_image = teca.generation.chooseImage
    logging.debug("generateCovers called with path={0} - files:{1}".format(path, files))

    filename=cfg.cover_image_name(path) #if it's chosen in conf, let's pick it
    if filename == "": #no cover images chosen for this folder
        logging.debug("choose_image path: {0}".format(os.path.join(cfg.starting_path, path)))
        filename = choose_image(os.path.join(cfg.starting_path, path), files, cfg)
    logging.debug("selected filename: {0}".format(filename))
    full_filename = os.path.join(path, filename)
    logging.debug("image {0} chosen for path {1}".format(full_filename, path))

    try:
        cover_obj = Image.open(full_filename)
    except IOError:
        #TODO: probably it could fail if launching Teca from another folder
        raise NotImplementedError("pls ask alfa to fix it, it's freaking stupid! ;_;")
        logging.debug("image {0} not found, looking {1}".format(full_filename, os.path.join(os.path.abspath(""), filename)))
        cover_obj = Image.open(os.path.join(os.path.abspath(""), filename))

    cover_obj.thumbnail(cfg.cover_size(path))
    cover_obj.save(os.path.join(path, "cover_.png"))


def generateThumbnails(path, files, cfg):
    for filename in files:
        full_filename = os.path.join(path, filename)
        if not cfg.regenerate_thumbnails and os.path.exists(os.path.join(path, "thumb_"+filename)):
            logging.debug("not generated the thumbnail for %s"%full_filename)
            continue
        logging.debug("generating thumbnail for %s"%full_filename)
        try:
            thumbnail_obj = Image.open(full_filename)
            thumbnail_obj.thumbnail(cfg.thumbnail_size(path))
            thumbnail_obj.save(os.path.join(path, "thumb_"+filename))
            logging.debug("generated thumbnail for {0}".format(full_filename))
        except Exception as e:
            logging.error("[Thumbnails]: error while generating thumbnail for {0}: {1}".format(full_filename,
                                                                                                          e))


def generateIndex(path, files, dirs, cfg):
    """
    this is the function that generates the HTML page
    that will be shown to the user
    """
    logging.debug("directories: "+"\n\t".join(dirs))
    logging.debug("files: "+"\n\tinserted: ".join(files))
    logging.debug("{0} -> >{1}< {2}".format(path, cfg.template_path(path), cfg.config.config["template_path"]))

    try:
        if cfg.short_links.use_feature:
            shortlinks_use_feature = True
            shortlinks_url = cfg.short_links.short_url
            tokens = json.load(open(cfg.short_links.links_database))
            urls = map(lambda fname: cfg.short_links.short_url+tokens[os.path.join(path, fname)], files)
        else:
            urls = files
            shortlinks_use_feature = False
            shortlinks_url = ""
    except AttributeError:
        urls = files
        shortlinks_use_feature = False
        shortlinks_url = ""
    import codecs
    codecs.open(os.path.join(path, "index.html"), "w", encoding = 'utf-8').write(
            jinja2.Template(
            open(cfg.template_path(path)).read()
                ).render(
                title = cfg.title(path),
                files = urls,
                images =  files,
                dirs = dirs,
                path = path,
                back_folder = not path and "" or "..",
                dirs_no = cfg.directories_on_a_row,
                images_no = cfg.images_on_a_row,
                use_symlink = shortlinks_use_feature,
                symlink_path = shortlinks_url
            )
        )

def goDeeper(starting_path, cfg):
    #for actual_dir, dirs, files in os.walk(starting_path, topdown=True):
    #    actual_dir = actual_dir #unicode_it(actual_dir, "utf8")
    #    if cfg.use_verbose:
    #        print(('walking into directory: ', actual_dir))
    #    files[:] = [unicode(f) for f in filterImages(files, cfg)
    #                     if f not in cfg.excluded_files(actual_dir)
    #                     and not cfg.excluded_file_formats(f)]
    #    #won't walk into some "excluded paths" (if needed)
    #    dirs[:] = [unicode(d) for d in dirs if d not in cfg.excluded_folders(actual_dir)]
    #    if cfg.use_verbose:
    #        print('now generating index...')
    #    generateThumbnails(actual_dir, files, cfg)
    #    generateCovers(actual_dir, files, cfg)
    #    generateThumbnails(actual_dir, files, cfg)
    #    generateIndex(actual_dir, files, dirs, cfg)
    for actual_dir, dirs, files in teca.filesystem.walk(starting_path, cfg):

        logging.debug("walking into directory %s", actual_dir)

        generateThumbnails(actual_dir, files, cfg)
        generateCovers(actual_dir, files, cfg)
        #generateShortLinks(actual_dir, files, dirs, cfg)
        generateIndex(actual_dir, files, dirs, cfg)


if __name__ == "__main__":
    options = handleCmd()
    cfghandler = ConfigHandler(options['cfgpath'], options)
    goDeeper(options['starting_path'], cfghandler)
