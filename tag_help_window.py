# coding: utf-8
#
# Copyright © 2019 Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#

import tkinter
from tkinter import Text
from tkinter import font as tkfont

class TagHelpWindow(tkinter.Toplevel):
    """
    Independent top level window for displaying ID3 tag help
    """
    def __init__(self, parent, x=0, y=0, width=100, height=100, close=None):
        """
        Create top level window containing tag help
        :param parent: Prent widget
        :param x: Where to position window
        :param y: Where to position window
        :param width: width of window in px
        :param height: height of window in px
        :param close: callback for window close event
        """
        help_lines = self._help_text().splitlines()
        longest_line = ""
        for line in help_lines:
            if len(line) > len(longest_line):
                longest_line = line

        super(TagHelpWindow, self).__init__(parent, width=width, height=height)
        self.on_close = close
        self.title("Tag Help")

        # TODO Use font to determine needed height
        f = tkfont.Font(self, family="Courier New", size=14)
        metrics = f.metrics()
        line_height = metrics["linespace"] + 1
        char_width = f.measure(longest_line) + f.measure("\n")
        self.geometry(newGeometry="{0}x{1}+{2}+{3}".format(char_width, int(len(help_lines) * line_height), x, y))
        self.resizable(width=True, height=True)
        self.deiconify()
        # Need to handle window close event to reset
        self.protocol("WM_DELETE_WINDOW", self._on_tag_help_close)

        # widgets

        self._text_widget = Text(self, width=int(width / 10), height=len(help_lines), bd=0, font=f)
        self._text_widget.grid(row=0, column=0, sticky=tkinter.NSEW)
        self._text_widget.insert(tkinter.END, self._help_text())
        self._text_widget.config(state=tkinter.DISABLED)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _on_tag_help_close(self):
        if self.on_close:
            self.on_close()
        self.destroy()
        return True

    def show(self):
        # This seems like overkill, but it's the best known solution
        # to bring the help window to the top and activate it
        self.lift()
        self.grab_set()
        self.focus()
        self.grab_release()

    def _help_text(self):
        """
        Interim help information
        :return:
        """
        return """
Currently Supported Tags
-----------------------
COMM: Comment
TALB: Album title
TBPM: Tempo (beats per minute)
TCON: Content type
TCOP: Copyright message
TDAT: Date
TDRC: Recording time
TFLT: File type
TIT1: Content group description
TIT2: Title/songname/content description
TIT3: Subtitle/description refinement
TPE1: Lead performer/soloist(s)
TPE2: Band/orchestra/accompaniment
TPE3: Conductor/performer refinement
TPE4: Interpreted, remixed, or otherwise modified by
TPOS: Part of set
TRCK: Track number/position in set

More information
----------------
http://id3.org/id3v2.3.0#Declared_ID3v2_frames
"""
