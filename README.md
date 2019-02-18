# ![ID3Tag Logo](resources/id3tag.gif) pyid3tag - Basic ID3 Tag Editor
Copyright © 2019 by Dave Hocker

## Overview
This app is a very basic ID3 tag editor for mp3 files. It is written in Python 3 
using TkInter and
should run of Windows, Linux or macOS X. For macOS X, there is an app (pyid3tag.app).
For other OSes, it can be run from the source.

## License

This app is licensed under the GNU General Public License v3 as published 
by the Free Software Foundation, Inc..
See the LICENSE file for the full text of the license.

## Running the App
### macOS X
The release includes a .zip file with pyid3tag.app. You can unzip it and copy the
pyid3tag.app file to the Applications folder. From there, you can run it using normal
macOS methods. For example, you can open a Finder window, go to Applications and double
click on the app file. Or, you can use LaunchPad.

### From Source
#### Requirements
You can use a virtual environment (hightly recommended) or you can install the 
requirements to the system Python 3. Virtual environments is out of the scope of
this discussion, but you can find out more from the [references](#references).

    cd pyid3tag
    pip install -r requirements.txt

Using this technique, you can run the app from its souce directory.

    cd pyid3tag
    python3 id3tag.py

## References <a id="references"></a>
* [virtualenv on pypi](https://virtualenv.pypa.io/en/latest/)
* [virtualenvwrapper read-the-docs](https://virtualenvwrapper.readthedocs.io/en/latest/)
