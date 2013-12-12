Teca
====

A simple static -and configurable- image gallery generator.

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
cp Teca/clean.sh $screenshot_folder
cd $screenshot_folder
sh clean.sh
echo "Thank you for using Teca"
```

Dependencies
===
* Jinja2 (from the Cheese Shop)
* optparse (stdlib)

TODO
===
Teca will be rebuilt, keeping in mind that
Jinja2 will be in charge of the generation of the html.

also, Teca will have some cool command-line features.
Configuration files will be written in JSON: Python has a parser
in the stdlib, so KISS and JSON ^_^