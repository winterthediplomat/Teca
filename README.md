Teca
====

A simple static -and configurable- image gallery generator.

DISCLAIMER
==========
IT'S A F**KIN' ALPHA, SO IT COULD DIVIDE BY ZERO AND DESTROY THE LIFE AS WE KNOW IT.
also, Teca code could be heavily modified very fast.
I told ya man, keep an eye on what you're doing.

Installation and Usage
===
```sh
git clone https://github.com/alfateam123/Teca.git
cd Teca
python teca.py $screenshots_folder
echo "Thank you for using Teca"
```

Remove the gallery
==
```sh
python clean.py $screenshots_folders
echo "Thank you for using Teca"
```

Configuration
===
it's all in the cfg.json file.
See Configuration.md file for every information you may need.

Dependencies
===
* Jinja2 (from the Cheese Shop or github)
* PIL (from the PythonWare site)
* optparse (stdlib)

I didn't try (Pillow)[https://github.com/python-imaging/Pillow], probably it could be a better option.
PIL is needed only for thumbnails: probably it's an overkill, even ImageMagick could be OK for this.
Duh, I'll investigate.

TODO
===
* refactor Teca
* write configuration documentation
* do a stylesheet. or at least, build a better UI.