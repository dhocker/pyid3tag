#! /bin/bash

# Build macOS X version of pyid3tag app

source `which virtualenvwrapper.sh`
workon pyid3tag
python setup.py py2app
deactivate
