#-*- coding:utf8 -*-

import os
import sys
import re
import string

###############################################################
############## CONFIGURATION ZONE #############################
## putting hands outside of this zone is just a YOUR PROBLEM ##
excluded = ['.git']
image_formats = ["jpg", "tiff", "png", "svg"]
kool_neims = {
        '.': 'MAH ROOT'
    }

fullbody_template = string.Template("""<html>
<head>
    <title>$path - Teca</title>
    <script>
    var hideImage=function(filepath)
    {document.getElementById("image_"+filepath).style.display='none';}
    var showImage=function(filepath)
    {document.getElementById("image_"+filepath).style.display='inherit';}
    var toggleImage=function(filepath)
    {
        var actual_display = document.getElementById(
            "image_"+filepath).style.display;
        if (actual_display == 'none')
            showImage(filepath);
        else if (actual_display == 'inherit')
            hideImage(filepath);
    }
    </script>
</head>
<body>
    <a href='../index.html'>Back to $upper_folder</a>
    <div id="folders"><ul>$folders</ul></div>
    <div id="images"><ul>$images</ul></div>
    <footer>You know what's cool? Lukhash and teca.py are cool!
    ah, alfateam123 wrote teca.py, blame him.</footer>
</body>
</html>"""
)

folder_template = string.Template(
    """<li><a href="$link_to_folder/index.html">$folder_name</a></li>""")
no_folders_template = string.Template(
    """<h4>You can't go deeper.</h4>"""
    )

image_template = string.Template("""<li><a href="#"
                onclick="toggleImage('$orig_image')">Show/Hide $orig_image</a>
                <img id="image_$orig_image" style='display:none'
                src="$orig_image" /></li>""")
no_images_template = string.Template(
    """<h4>no images to show here.</h4>"""
    )
############ END CONFIGURATION ZONE ###########################
###############################################################


def filterImages(files):
    """this function just filter images using given image formats."""
    regex = "\.(" + "|".join(image_formats) + ")$"
    #filter(lambda s: re.match(regex, s), files)
    return [s for s in files if re.findall(regex, s)]


def generateIndex(path, files, dirs):
    """
    this is the function that generates the HTML page
    that will be shown to the user
    """
    #preparing the index
    index_file = open(os.path.join(path, "index.html"), "w")

    template_params = {'path': path,
                       'images': '',
                       'folders': '',
                       'upper_folder': ''}
    
    #making upper folder right.
    head, tail = os.path.split(path)
    if tail == '':
        head = (os.path.sep).join(head.split(os.path.sep)[:-1])
    template_params['upper_folder'] = head

    #let's see if path has a cool name
    try:
        template_params['path'] = kool_neims[path]
    except KeyError:
        pass

    #write the folders
    if not dirs:
        template_params['folders'] = no_folders_template.safe_substitute()
    for dir_ in dirs:
        try:
            cool_folder_name = kool_neims[dir_]
        except KeyError:
            cool_folder_name = dir_.replace('_', ' ').capitalize()

        template_params['folders'] += folder_template.safe_substitute(
                                link_to_folder="%s" % (dir_),
                                folder_name=cool_folder_name)

    #put the files into page
    #files are all images. in case, just replace with filterImages(files)
    if not files:
        template_params['images'] = no_images_template.safe_substitute()
    for image in files:
        template_params['images'] += image_template.safe_substitute(
                                      orig_image=image
                                      )

    #closing the file and saving modifications
    index_file.write(fullbody_template.safe_substitute(template_params))
    index_file.close()


def goDeeper(starting_path):
    for root, dirs, files in os.walk(starting_path, topdown=True):
        files[:] = filterImages(files)
        #won't walk into some "excluded paths" (if needed)
        dirs[:] = [d for d in dirs if d not in excluded]

        generateIndex(root, files, dirs)

if __name__ == "__main__":
    spath = sys.argv[-1]
    goDeeper(spath)
