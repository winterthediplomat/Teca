Teca Configuration
==================

Purpose
------------
Teca is a simple, static and configurable image gallery generator.

Pratically everything in Teca is configurable. This leads to a complex configuration file: this document is here to explain it to you.

Folder parameters
-----------------
**paths**: a dictionary (FolderName, FolderDescription).

**image_formats**: This is a list of image extensions. It's used by Teca for selecting images only. Every file that does not have this extension will be ignored. 

This parameter is _not optional_. Please, don't add formats that PIL and Pillow are not able to manipulate (like video or audio or documents formats).

example:
```
["jpg", "gif", "png"]
```

**excluded_files**: This is a list of file names. Files that are in this list won't be shown in generated files.

This parameter is _optional_, by default it's an empty list.

**excluded_file_formats**: This is a list of regular expressions. Files that matches these regular expressions will be ignored and not shown in the list. Mostly used for Teca internals.

This parameter is _not optional_, at least at root level. If you're not sure about it, just don't modify it.

_Note:_ the rules defined at root are valid for every subfolder. If you want to overwrite the rules for a folder, you have to re-define the parameter in the subfolder description. This overwrite is not reflected to folder's children.

example:
```
["^thumb_", "^cover_"]
```

**title**: This is a fixed name for the folder. It will be shown in the dedicated index page.

This parameter is _optional_: by default, the title will be a capitalized string where underscores are replaced with whitespaces.

example:
```
"just a cool name for this folder"
#default
$MAH_FOLDER/cool/folder/name_you_got -> "Name you got"
```

**cover_image_size**: This is a dictionary containing the size of a cover image. A cover image is the image that Teca shows for giving a preview of the folder.

This parameter is _not optional_, at least at root level.

_Note:_ the rules defined at root are valid for every subfolder. If you want to overwrite the rules for a folder, you have to re-define the parameter in the subfolder description. This overwrite is not reflected to folder's children.

example:
```
"cover_size": {
        "width": 640,
        "height": 400
    }
```

**thumbnail_size**: This is a dictionary containing the size of a thumbnail. A thumbnail is an image that gives you a preview of the real image.

This parameter is _not optional_, at least at root level.

_Note:_ the rules defined at root are valid for every subfolder. If you want to overwrite the rules for a folder, you have to re-define the parameter in the subfolder description. This overwrite is not reflected to folder's children.

example:
```
"cover_size": {
        "width": 640,
        "height": 400
    }
```

**regenerate_thumbnails**: This is a flag for telling Teca if regenerate thumbnails or not.

This parameter is _not optional_, and it must be valorized at root level. Overwrites at lower levels are not given a f**k.

_Note_: If you changed the thumbnail size and didn't see any change in the generated files, probably it's set to ```false```. Set it to ```true``` and relaunch Teca, it should change the thumbnail size in the generated files. 

**template_path**: this is the path of the template file. Maybe you can want a different template in a different folder: set this parameter in the related folder description to the template you want to use.

This parameter is _not optional_, at least at root level.

_Note:_ the rules defined at root are valid for every subfolder. If you want to overwrite the rules for a folder, you have to re-define the parameter in the subfolder description. This overwrite is not reflected to folder's children.

**directories_on_a_row_**: this is the number of cover images that must be shown in a row.

This parameter is _optional_, by default is 1.

_Note:_ the rules defined at root are valid for every subfolder. If you want to overwrite the rules for a folder, you have to re-define the parameter in the subfolder description. This overwrite is not reflected to folder's children.

**images_on_a_row_**: this is the number of thumbnails that must be shown in a row.

This parameter is _optional_, by default is 1.

_Note:_ the rules defined at root are valid for every subfolder. If you want to overwrite the rules for a folder, you have to re-define the parameter in the subfolder description. This overwrite is not reflected to folder's children.

**default_image**: this is the path of the default image.

This image will be used in case a folder (and its inner folders) does not have images.

This parameter is _not optional_, at least at root level.