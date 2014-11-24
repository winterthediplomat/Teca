#!/usr/bin/env python

from __future__ import print_function
import os
import json
from pathlib import PosixPath
import random
from string import ascii_lowercase
import sys

def onerror(*args):
  print(args)

token_list = dict()
def random_token(token_lenght=7, alphabet=ascii_lowercase+"0123456789"):
  while True:
    muh_token = "".join(random.sample(alphabet, token_lenght))
    if not muh_token in token_list:
      token_list[muh_token] = muh_token
      return muh_token
  

if __name__ == "__main__":
  try:
    path_to_tokenize = sys.argv[1]
    path_of_symlinks = sys.argv[2]
  except IndexError:
    print("no paths inserted, shutting down.")
    sys.exit(1)

  try:
    already_linked_images = json.load(open("links.json"))
  except IOError:
    print("can't open links.json!")
    already_linked_images = dict()

  for path, folders, files in os.walk(path_to_tokenize, followlinks=True, onerror=onerror):
    files_ = map(lambda x: os.path.join(path, x), files)
    for file_ in files_:
      if PosixPath(file_).name.startswith("thumb_") or PosixPath(file_).name.startswith("cover_"):
        continue
      if not  file_ in  already_linked_images:
        dat_token = random_token()
        os.symlink(file_, os.path.join(path_of_symlinks, dat_token))
        already_linked_images[file_] = dat_token
        print("connected image", file_, "to token", dat_token)

  json.dump(already_linked_images, open("links.json", "w"))
  print("done.")
