#-*- coding:utf8 -*-

from teca import *
import os

#this is the original. it does not work with spaces.
"""function cleanFolder {
  for dir in $(find . -mindepth 1 -type d | grep -v .git); do
    echo "going into $dir"
    #cd $dir;
    rm "$dir/index.html";
    #cleanFolder;
  done
}

cleanFolder
"""

if __name__ == "__main__":
    options = handleCmd()
    cfg = ConfigHandler(options['cfgpath'], options)
    for actual_dir, dirs, files in os.walk(options['starting_path'], topdown=True):
        if cfg.use_verbose:
            print(('walking into directory: ', actual_dir))
        files[:] = [f for f in filterImages(files, cfg)
                         if not (f not in cfg.excluded_files(actual_dir)
                         and not cfg.excluded_file_formats(f))]
        #won't walk into some "excluded paths" (if needed)
        dirs[:] = [d for d in dirs if d not in cfg.excluded_folders(actual_dir)]

        for file_to_delete in files:
        	os.remove(os.path.join(actual_dir, file_to_delete))
        try:
        	os.remove(os.path.join(actual_dir, "index.html"))
        except OSError:
        	pass

