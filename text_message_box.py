# coding: utf-8
#
# Modal text message box similar to tkmessagebox
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

import os
import tkinter
from tkinter import Text, Scrollbar, Button, Frame, Label
from tkinter import font as tkfont
import PIL.Image
import PIL.ImageTk

class TextMessageBox(tkinter.Toplevel):
    """
    Independent top level window for displaying ID3 tag help
    """
    def __init__(self, parent,
                 title="Text Message Box", text=None, heading=None,
                 font="TkDefaultFont",
                 x=None, y=None, width=100, height=100,
                 image=None,
                 close=None):
        """
        Create top level window containing tag help
        :param parent: Parent widget
        :param title: The message box window title
        :param text: The text to be displayed in the body of the message box
        :param heading: Heading line for the body text
        :param font: The font to be used within the message box
        :param x: Where to position window. Default is center screen.
        :param y: Where to position window. Default is center screen.
        :param width: width of window in px
        :param height: height of window in px
        :param image: image to be display in message box
        :param close: callback for window close event
        """
        super(TextMessageBox, self).__init__(parent, width=width, height=height)

        longest_line = ""
        if text:
            text_lines = text.splitlines()
            for line in text_lines:
                if len(line) > len(longest_line):
                    longest_line = line

        self.on_close = close
        self.title(title)

        # Logo image
        self._image = None
        if image and os.path.exists(image):
            self._image = PIL.ImageTk.PhotoImage(file=image)

        # Use font to determine needed height
        f = tkfont.Font(self, font=font)

        metrics = f.metrics()
        line_height = metrics["linespace"] + 1
        padx = 25
        pady = line_height
        # Most of these numbers were determined empirically
        # The width is the longest line w/line-end plus 15% + padding
        char_width = int(float(f.measure(longest_line) + f.measure("\n")) * 1.15) + int(padx * 2)
        # The height is set at a max of 40 lines with 2 lines for padding
        max_text_height = min(len(text_lines), 40) + 2
        # The window height includes the button, logo image and more padding
        max_window_height = max_text_height  + int((pady * 5) / line_height)
        if self._image:
            max_window_height += int(self._image.height() / line_height)

        # Determine origin of the window, in the middle of the screen
        if x is None and y is None:
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            x = int((sw / 2) - (char_width / 2))
            y = int((sh / 2) - (max_window_height * line_height / 2))

        self.geometry(newGeometry="{0}x{1}+{2}+{3}".format(char_width, int(max_window_height * line_height), x, y))
        self.resizable(width=True, height=True)
        self.deiconify()
        # Need to handle window close event to reset
        self.protocol("WM_DELETE_WINDOW", self._on_tag_help_close)

        # widgets

        self._frame = Frame(self, width=int(char_width / f.measure("M")), height=max_text_height,
                            bd=0, relief=tkinter.GROOVE)
        self._frame.grid(row=0, column=0, sticky=tkinter.NSEW, padx=5, pady=5)
        self._frame.grid_columnconfigure(0, weight=1)

        self._text_widget = Text(self._frame, width=int(char_width / f.measure("M")), height=max_text_height, bd=0, font=f)
        self._text_widget.grid(row=0, column=0, sticky=tkinter.NSEW, padx=padx, pady=pady)

        # If there is a heading, display it in bold
        if heading:
            self._text_widget.insert(tkinter.END, heading + "\n")
            self._text_widget.tag_add("heading", 1.0, 2.0)
            bold_font = tkfont.Font(self, family=font, size=14, weight="bold")
            self._text_widget.tag_config("heading", font=bold_font)

        # Insert the text body
        self._text_widget.insert(tkinter.END, text)
        # Make the text widget read-only
        self._text_widget.config(state=tkinter.DISABLED)

        self._scrollbar = Scrollbar(self._frame, command=self._text_widget.yview)
        self._scrollbar.grid(row=0, column=1, sticky=tkinter.NS)
        self._text_widget['yscrollcommand'] = self._scrollbar.set

        self._button = Button(self, text="Close", width=4, command=self._on_tag_help_close)
        self._button.grid(row=1, column=0, columnspan=2, pady=int(pady / 2), sticky=tkinter.S)

        # Avatar image
        # TODO Try different placements
        if self._image:
            self._avatar = Label(self, image=self._image)
            self._avatar.grid(row=2, column=0, columnspan=2)
            self._avatar._image = self._image

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _on_tag_help_close(self):
        """
        The message box is closing
        :return: Always returns True
        """
        if self.on_close:
            self.on_close()
        self.grab_release()
        self.destroy()
        return True

    def show(self):
        """
        Show the message box
        :return: None
        """
        # This seems like overkill, but it's the best known solution
        # to bring the help window to the top and activate it
        # as the topmost modal window
        self.lift()
        self.grab_set()
        self.focus()
