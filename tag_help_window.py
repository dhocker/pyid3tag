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

        # TODO Use font to determine needed height
        f = tkfont.Font(self, family="Courier New", size=10)
        metrics = f.metrics()
        line_height = metrics["linespace"] + 1
        char_width = f.measure(longest_line) + f.measure("\n")
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
4.20    AENC    [[#sec4.20|Audio encryption]]
4.15    APIC    [#sec4.15 Attached picture]
4.11    COMM    [#sec4.11 Comments]
4.25    COMR    [#sec4.25 Commercial frame]
4.26    ENCR    [#sec4.26 Encryption method registration]
4.13    EQUA    [#sec4.13 Equalization]
4.6     ETCO    [#sec4.6 Event timing codes]
4.16    GEOB    [#sec4.16 General encapsulated object]
4.27    GRID    [#sec4.27 Group identification registration]
4.4     IPLS    [#sec4.4 Involved people list]
4.21    LINK    [#sec4.21 Linked information]
4.5     MCDI    [#sec4.5 Music CD identifier]
4.7     MLLT    [#sec4.7 MPEG location lookup table]
4.24    OWNE    [#sec4.24 Ownership frame]
4.28    PRIV    [#sec4.28 Private frame]
4.17    PCNT    [#sec4.17 Play counter]
4.18    POPM    [#sec4.18 Popularimeter]
4.22    POSS    [#sec4.22 Position synchronisation frame]
4.19    RBUF    [#sec4.19 Recommended buffer size]
4.12    RVAD    [#sec4.12 Relative volume adjustment]
4.14    RVRB    [#sec4.14 Reverb]
4.10    SYLT    [#sec4.10 Synchronized lyric/text]
4.8     SYTC    [#sec4.8 Synchronized tempo codes]
4.2.1   TALB    [#TALB Album/Movie/Show title]
4.2.1   TBPM    [#TBPM BPM (beats per minute)]
4.2.1   TCOM    [#TCOM Composer]
4.2.1   TCON    [#TCON Content type]
4.2.1   TCOP    [#TCOP Copyright message]
4.2.1   TDAT    [#TDAT Date]
4.2.1   TDLY    [#TDLY Playlist delay]
4.2.1   TENC    [#TENC Encoded by]
4.2.1   TEXT    [#TEXT Lyricist/Text writer]
4.2.1   TFLT    [#TFLT File type]
4.2.1   TIME    [#TIME Time]
4.2.1   TIT1    [#TIT1 Content group description]
4.2.1   TIT2    [#TIT2 Title/songname/content description]
4.2.1   TIT3    [#TIT3 Subtitle/Description refinement]
4.2.1   TKEY    [#TKEY Initial key]
4.2.1   TLAN    [#TLAN Language(s)]
4.2.1   TLEN    [#TLEN Length]
4.2.1   TMED    [#TMED Media type]
4.2.1   TOAL    [#TOAL Original album/movie/show title]
4.2.1   TOFN    [#TOFN Original filename]
4.2.1   TOLY    [#TOLY Original lyricist(s)/text writer(s)]
4.2.1   TOPE    [#TOPE Original artist(s)/performer(s)]
4.2.1   TORY    [#TORY Original release year]
4.2.1   TOWN    [#TOWN File owner/licensee]
4.2.1   TPE1    [#TPE1 Lead performer(s)/Soloist(s)]
4.2.1   TPE2    [#TPE2 Band/orchestra/accompaniment]
4.2.1   TPE3    [#TPE3 Conductor/performer refinement]
4.2.1   TPE4    [#TPE4 Interpreted, remixed, or otherwise modified by]
4.2.1   TPOS    [#TPOS Part of a set]
4.2.1   TPUB    [#TPUB Publisher]
4.2.1   TRCK    [#TRCK Track number/Position in set]
4.2.1   TRDA    [#TRDA Recording dates]
4.2.1   TRSN    [#TRSN Internet radio station name]
4.2.1   TRSO    [#TRSO Internet radio station owner]
4.2.1   TSIZ    [#TSIZ Size]
4.2.1   TSRC    [#TSRC ISRC (international standard recording code)]
4.2.1   TSSE    [#TSEE Software/Hardware and settings used for encoding]
4.2.1   TYER    [#TYER Year]
4.2.2   TXXX    [#TXXX User defined text information frame]
4.1     UFID    [#sec4.1 Unique file identifier]
4.23    USER    [#sec4.23 Terms of use]
4.9     USLT    [#sec4.9 Unsychronized lyric/text transcription]
4.3.1   WCOM    [#WCOM Commercial information]
4.3.1   WCOP    [#WCOP Copyright/Legal information]
4.3.1   WOAF    [#WOAF Official audio file webpage]
4.3.1   WOAR    [#WOAR Official artist/performer webpage]
4.3.1   WOAS    [#WOAS Official audio source webpage]
4.3.1   WORS    [#WORS Official internet radio station homepage]
4.3.1   WPAY    [#WPAY Payment]
4.3.1   WPUB    [#WPUB Publishers official webpage]
4.3.2   WXXX    [#WXXX User defined URL link frame]
More information
----------------
http://id3.org/id3v2.3.0#Declared_ID3v2_frames
"""
