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
from tkinter import Text, Scrollbar
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

        # Use font to determine needed height
        f = tkfont.Font(self, font="TkFixedFont")

        metrics = f.metrics()
        line_height = metrics["linespace"] + 1
        char_width = int(float(f.measure(longest_line) + f.measure("\n")) * 1.1)
        max_height = min(len(help_lines), 40)
        self.geometry(newGeometry="{0}x{1}+{2}+{3}".format(char_width, int(max_height * line_height), x, y))
        self.resizable(width=True, height=True)
        self.deiconify()
        # Need to handle window close event to reset
        self.protocol("WM_DELETE_WINDOW", self._on_tag_help_close)

        # widgets

        self._text_widget = Text(self, width=int(width / 10), height=max_height, bd=0, font=f)
        self._text_widget.grid(row=0, column=0, sticky=tkinter.NSEW)
        self._text_widget.insert(tkinter.END, self._help_text())
        self._text_widget.config(state=tkinter.DISABLED)

        self._scrollbar = Scrollbar(self, command=self._text_widget.yview)
        self._scrollbar.grid(row=0, column=1, sticky=tkinter.NSEW)
        self._text_widget['yscrollcommand'] = self._scrollbar.set

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
ID3v2 Tags from http://id3.org/id3v2.3.0#Declared_ID3v2_frames
--------------------------------------------------------------
4.20\tAENC\t[[#sec4.20|Audio encryption]]
4.15\tAPIC\t[#sec4.15 Attached picture]
4.11\tCOMM\t[#sec4.11 Comments]
4.25\tCOMR\t[#sec4.25 Commercial frame]
4.26\tENCR\t[#sec4.26 Encryption method registration]
4.13\tEQUA\t[#sec4.13 Equalization]
4.6\tETCO\t[#sec4.6 Event timing codes]
4.16\tGEOB\t[#sec4.16 General encapsulated object]
4.27\tGRID\t[#sec4.27 Group identification registration]
4.4\tIPLS\t[#sec4.4 Involved people list]
4.21\tLINK\t[#sec4.21 Linked information]
4.5\tMCDI\t[#sec4.5 Music CD identifier]
4.7\tMLLT\t[#sec4.7 MPEG location lookup table]
4.24\tOWNE\t[#sec4.24 Ownership frame]
4.28\tPRIV\t[#sec4.28 Private frame]
4.17\tPCNT\t[#sec4.17 Play counter]
4.18\tPOPM\t[#sec4.18 Popularimeter]
4.22\tPOSS\t[#sec4.22 Position synchronisation frame]
4.19\tRBUF\t[#sec4.19 Recommended buffer size]
4.12\tRVAD\t[#sec4.12 Relative volume adjustment]
4.14\tRVRB\t[#sec4.14 Reverb]
4.10\tSYLT\t[#sec4.10 Synchronized lyric/text]
4.8\tSYTC\t[#sec4.8 Synchronized tempo codes]
4.2.1\tTALB\t[#TALB Album/Movie/Show title]
4.2.1\tTBPM\t[#TBPM BPM (beats per minute)]
4.2.1\tTCOM\t[#TCOM Composer]
4.2.1\tTCON\t[#TCON Content type]
4.2.1\tTCOP\t[#TCOP Copyright message]
4.2.1\tTDAT\t[#TDAT Date]
4.2.1\tTDLY\t[#TDLY Playlist delay]
4.2.1\tTENC\t[#TENC Encoded by]
4.2.1\tTEXT\t[#TEXT Lyricist/Text writer]
4.2.1\tTFLT\t[#TFLT File type]
4.2.1\tTIME\t[#TIME Time]
4.2.1\tTIT1\t[#TIT1 Content group description]
4.2.1\tTIT2\t[#TIT2 Title/songname/content description]
4.2.1\tTIT3\t[#TIT3 Subtitle/Description refinement]
4.2.1\tTKEY\t[#TKEY Initial key]
4.2.1\tTLAN\t[#TLAN Language(s)]
4.2.1\tTLEN\t[#TLEN Length]
4.2.1\tTMED\t[#TMED Media type]
4.2.1\tTOAL\t[#TOAL Original album/movie/show title]
4.2.1\tTOFN\t[#TOFN Original filename]
4.2.1\tTOLY\t[#TOLY Original lyricist(s)/text writer(s)]
4.2.1\tTOPE\t[#TOPE Original artist(s)/performer(s)]
4.2.1\tTORY\t[#TORY Original release year]
4.2.1\tTOWN\t[#TOWN File owner/licensee]
4.2.1\tTPE1\t[#TPE1 Lead performer(s)/Soloist(s)]
4.2.1\tTPE2\t[#TPE2 Band/orchestra/accompaniment]
4.2.1\tTPE3\t[#TPE3 Conductor/performer refinement]
4.2.1\tTPE4\t[#TPE4 Interpreted, remixed, or otherwise modified by]
4.2.1\tTPOS\t[#TPOS Part of a set]
4.2.1\tTPUB\t[#TPUB Publisher]
4.2.1\tTRCK\t[#TRCK Track number/Position in set]
4.2.1\tTRDA\t[#TRDA Recording dates]
4.2.1\tTRSN\t[#TRSN Internet radio station name]
4.2.1\tTRSO\t[#TRSO Internet radio station owner]
4.2.1\tTSIZ\t[#TSIZ Size]
4.2.1\tTSRC\t[#TSRC ISRC (international standard recording code)]
4.2.1\tTSSE\t[#TSEE Software/Hardware and settings used for encoding]
4.2.1\tTYER\t[#TYER Year]
4.2.2\tTXXX\t[#TXXX User defined text information frame]
4.1\tUFID\t[#sec4.1 Unique file identifier]
4.23\tUSER\t[#sec4.23 Terms of use]
4.9\tUSLT\t[#sec4.9 Unsychronized lyric/text transcription]
4.3.1\tWCOM\t[#WCOM Commercial information]
4.3.1\tWCOP\t[#WCOP Copyright/Legal information]
4.3.1\tWOAF\t[#WOAF Official audio file webpage]
4.3.1\tWOAR\t[#WOAR Official artist/performer webpage]
4.3.1\tWOAS\t[#WOAS Official audio source webpage]
4.3.1\tWORS\t[#WORS Official internet radio station homepage]
4.3.1\tWPAY\t[#WPAY Payment]
4.3.1\tWPUB\t[#WPUB Publishers official webpage]
4.3.2\tWXXX\t[#WXXX User defined URL link frame]

More information
----------------
http://id3.org/id3v2.3.0#Declared_ID3v2_frames
"""
