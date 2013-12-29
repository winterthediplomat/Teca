#-*- coding:utf8 -*-

#stdlib
import os
import re
import json
import random
from optparse import OptionParser
#external libraries
import jinja2
from PIL import Image



class ConfigHandler(object):

    def __init__(self, config_json_path=None, options_from_cmd=None):
        if config_json_path:
            self.config = json.load(open(config_json_path))
        else:
            B
            self.config = {
                "image_formats":[
                    "jpg", "tiff", "png", "bmp"
                    ],
                "excluded_folders":[
                ]
            }
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

    #@property
    def excluded_folders(self, path):
        return self._get_obj_from_path(path)["excluded_folders"]

    #@property
    def excluded_files(self, path):
        return self._get_obj_from_path(path)["excluded_files"]

    def excluded_file_formats(self, filename):
        return any(
                map(
                    lambda regex_format: re.match(regex_format, filename), 
                    self.config["excluded_file_formats"]
                    )
                )

    def _get_obj_from_path(self, path):
        """
        Internal
        """
        #paths are in this format:
        #other/another/more/folder/name
        #and, in file, it's like
        #"paths":{"other":{"another":{"more":{"folder":{"name":{}}}}}}
        #for i in os.split
        obj_from_path = self.config["paths"]
        try:
            for subpath in filter(bool, path.split(os.path.sep)):
                obj_from_path = obj_from_path[subpath]
        except KeyError: #we give a default
            obj_from_path = {
                "title": filter(bool, path.split(os.path.sep))[-1].capitalize(),
                "excluded_folders": [],
                "excluded_files": []
            }
        return obj_from_path

    #@property
    def title(self, path):
        """
        returns the title to display when referring
        to the folder with the given path.
        paths should be like
        > "anime/yahari"
        > "games/ff14"
        """
        return self._get_obj_from_path(path)["title"]

    def cover_image_name(self, path):
        try:
            return self._get_obj_from_path(path)["cover_image"]
        except KeyError:
            return ":random" #":" sign in a filename is not allowed in the major filesystems.

    def thumbnail_size(self, path):
        try:
            thumb_size_dict = self._get_obj_from_path(path)["thumbnail_size"]
        except KeyError:
            thumb_size_dict = self.config["thumbnail_size"]
        return (thumb_size_dict["width"], thumb_size_dict["height"])

    def cover_size(self, path):
        try:
            cover_size_dict = self._get_obj_from_path(path)["cover_size"]
        except KeyError:
            cover_size_dict = self.config["cover_size"]
        return (cover_size_dict["width"], cover_size_dict["height"])

    @property
    def image_prefix_path(self, path):
        """
        fool idea: allowing links on other sites.
        it's transparent for the end user.
        """
        try:
            return self._get_obj_from_path(path)["fspath"]
        except IndexError:
            return ""

    @property
    def regenerate_thumbnails(self):
        return self.config["regenerate_thumbnails"]
    

    @property
    def template_path(self):
        return self.config["template_path"]

    @property
    def directories_on_a_row(self):
        try:
            return self.config["directories_on_a_row"]
        except KeyError:
            return 1
    
    @property
    def images_on_a_row(self):
        try:
            return self.config["images_on_a_row"]
        except KeyError:
            return 1


def filterImages(files, cfg):
    """this function just filter images using given image formats."""
    regex = "\.(" + "|".join(cfg.image_formats) + ")$"
    #filter(lambda s: re.match(regex, s), files)
    return [s for s in files if re.findall(regex, s)]


def generateCovers(path, files, cfg):
    filename=cfg.cover_image_name(path)
    if filename == ":random":
        try:
            filename = random.choice(files)
        except IndexError:
            return None
    full_filename = os.path.join(path, filename)
    cover_obj = Image.open(full_filename)
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

    open(os.path.join(path, "index.html"), "w").write(
            jinja2.Template(
            open(cfg.template_path).read()
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
        if cfg.use_verbose:
            print(('walking into directory: ', actual_dir))
        files[:] = [f for f in filterImages(files, cfg)
                         if f not in cfg.excluded_files(actual_dir)
                         and not cfg.excluded_file_formats(f)]
        #won't walk into some "excluded paths" (if needed)
        dirs[:] = [d for d in dirs if d not in cfg.excluded_folders(actual_dir)]
        if cfg.use_verbose:
            print('now generating index...')
        generateCovers(actual_dir, files, cfg)
        generateThumbnails(actual_dir, files, cfg)
        generateIndex(actual_dir, files, dirs, cfg)


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
