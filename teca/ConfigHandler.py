import os
import sys
import re
import json
import random

class FolderConfig(object):
    
    def __init__(self, dict_config=None):
        for conf_key, conf_value in (dict_config or dict()).iteritems():
            self.__dict__[conf_key]=conf_value

    @property
    def config(self):
        return self.__dict__

    def __getitem__(self, attr_name):
        """enables the obj['key']-style attribute access"""
        return self.__dict__[attr_name]

    def merge_with(self, father_obj=None):
        #print "merge result: ", dict(list(father_obj.config.iteritems())+list(self.config.iteritems()))
        self.__dict__ = dict(list(father_obj.config.iteritems())+list(self.config.iteritems()))

    def __str__(self):
        return repr(self.config)
    
    def __repr__(self):
        return repr(self.config)

class ConfigHandler(object):

    def __init__(self, config_json_path=None, options_from_cmd=None):
        if config_json_path:
            self.config = self.adapt(json.load(open(config_json_path)))
        else:
            self.config = FolderConfig({
                "image_formats":[
                    "jpg", "tiff", "png", "bmp"
                    ],
                "excluded_folders":[
                ]
            })
        if options_from_cmd:
            self.cmd_config = options_from_cmd
        else:
            self.cmd_config = dict()

    def adapt(self, config_dict, father_obj=None, ind=0):
        """Internal"""
        #return config_dict

        #if we're called, we are sure that the json is valid and a valid config_dict has been generated
        #print "config_dict: ", config_dict
        root_cfg = FolderConfig(config_dict)
        #print "root before merge: ", root_cfg
        if father_obj: father_obj.paths = dict()
        root_cfg.merge_with(father_obj or FolderConfig()) #add values that are not defined in children
        #print "father: ", father_obj

        #print "root after merge: ", root_cfg
        converted_paths=dict()
        for subfolder_name, subfolder_config in root_cfg.paths.iteritems():
            #print '\t'*ind+"going to adapt {0}.".format(subfolder_name, root_cfg)
            converted_paths[subfolder_name] = self.adapt(subfolder_config, root_cfg, ind+1)
            #print '\t'*ind+"[DEBUG]: {0}".format(converted_paths.keys())
        root_cfg.paths=converted_paths
        #root_cfg.paths = dict((subfolder_name, self.adapt(subfolder_config, root_cfg)) for subfolder_name, subfolder_config in root_cfg.paths.iteritems())
        return root_cfg

    @property
    def use_verbose(self):
        return self.cmd_config["verbose"]

    @property
    def image_formats(self):
        return self.config["image_formats"]

    #@property
    def excluded_folders(self, path):
        try:
            return self._get_obj_from_path(path)["excluded_folders"]
        except KeyError:
            return list()

    #@property
    def excluded_files(self, path):
        try:
            return self._get_obj_from_path(path)["excluded_files"]
        except KeyError:
            return list()

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
        obj_from_path = self.config.config #self.config["paths"]
        try:
            for subpath in filter(bool, path.split(os.path.sep)):
                obj_from_path = obj_from_path["paths"][subpath]
        except KeyError:
            print "[warning] got an error while retrieving the object, path: {0}".format(path)
            obj_from_path = dict()
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
        try:
            return self._get_obj_from_path(path)["title"]
        except KeyError:
            #doing some fast modification to folder name, using it as a default
            print "[warning] not found a title for {0}".format(path)
            return path.split(os.path.sep)[-1].replace("_", " ").capitalize()

    def cover_image_name(self, path):
        try:
            return self._get_obj_from_path(path)["cover_image"]
        except KeyError:
            return ":random" #":" symbol in a filename is not allowed in the major filesystems.

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
    
    def template_path(self, path):
        try:
            return self._get_obj_from_path(path)["template_path"]
        except KeyError:
            print "[warning]: got a key error retrieving template_path for {0}, using default".format(path)
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

    @property
    def algorithm(self):
        try:
            return self.config["algorithm"]
        except KeyError:
            return 'md5'