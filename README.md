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
* Pillow (from the Cheese Shop or github)
* optparse (stdlib)

30 dec 2013: officially switched to Pillow
```
<Robertof> alfateam123
<Robertof> :: Vuoi sostituire python2-imaging con community/python2-pillow? [S/n] s
<Robertof> io faccio y
<alfateam123> Robertof: massì, prova
<alfateam123> sostituisci
<Robertof> già fatto alfateam123 
<alfateam123> lol
```

TODO
===
* refactor Teca
* write configuration documentation
* do a stylesheet. or at least, build a better UI.
