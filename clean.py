#-*- coding:utf8 -*-

from teca.ConfigHandler import ConfigHandler
from teca.utils import handleCmd, filterImages
import os

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

