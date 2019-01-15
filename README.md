# OSK Kurs
A website designed and created for driving school OSK Kurs in Świdnik.
Soon you'll have the possibility to see it on http://osk-kurs.pl/ ;)

### Some features
  - signing up for a course with an e-mail notification system
  - CMS with creating, editing and deleting courses and exporting them to PDF
  - editing and updating some basic data included in main website

### Tech

This app uses technologies like:
* [Python3.6](https://www.python.org/) - basic programming language
* [Flask 1.0.2](http://flask.pocoo.org/) - my favourite microframework for Python
* [MaterializeCSS](https://materializecss.com/) - my favourite library for front-end
* and maybe some other but I don't remember now ;)

### Installation

It requires Python 3.6 to run. 

Firsty, create somewhere your virtual environment for this project [check this out](https://docs.python.org/3/library/venv.html) and activate it:
```sh
$ python3 -m venv /path/to/new/virtual/environment
$ source  [path]/venv/bin/activate
```
Then, using *pip*, install ald dependencies from included file [check this out](https://stackoverflow.com/questions/7225900/how-to-install-packages-using-pip-according-to-the-requirements-txt-file-from-a):
```sh
$ pip install -r /path/to/requirements.txt
```
You may need *setup-tools* if you don't have it.
Then run the app on *localhost* (*Ubuntu*):
```sh
$ python3 path/to/project/run.py
```
### Credits
All rights deserved to Patryk Samborski &#169; 2019. Nevertheless - get inspired :D

I also recommend tutorials by [Corey Schafer](https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g) - they helped a lot with my project! [(his Github)](https://github.com/CoreyMSchafer)
