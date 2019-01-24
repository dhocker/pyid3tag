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
# Attribution
# Adapted from https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
#

from tkinter import Label, Toplevel


class ToolTipPopup():
    '''
    create a tooltip for a given parent widget
    '''
    def __init__(self, widget, text='widget info',
                 fg="black", bg="#a6e1fc", auto_close=3000,
                 dx=25, dy=20):
        """
        Create a tool tip instance
        :param widget: parent widget
        :param text: the tool tip text
        :param fg: foreground color, default black
        :param bg: background color, default light blue
        :param auto_close: time in ms until tool tip automatically closes
        :param dx: tooltip x offset from parent widget origin, default 25px
        :param dy: tooltip y offset from parent widget origin, default 20px
        """
        self._widget = widget
        self._text = text
        self._fg = fg
        self._bg = bg
        self._auto_close = auto_close
        self._dx = dx
        self._dy = dy
        self._tw = None
        self._widget.bind("<Enter>", self.enter)
        self._widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        """
        Captures hover over the parent widget
        :param event:
        :return: None
        """
        x = 0
        y = 0
        # bbox returns a 4-tuple (x, y, width, height)
        x, y, cx, cy = self._widget.bbox("insert")
        # Offset tool tip from parent widget
        x += self._widget.winfo_rootx() + self._dx
        y += self._widget.winfo_rooty() + self._dy
        # creates a toplevel window
        self._tw = Toplevel(self._widget)
        # Leaves only the label and removes the app window
        self._tw.wm_overrideredirect(True)
        self._tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self._tw, text=self._text, justify='left',
                      fg=self._fg, bg=self._bg, relief='solid', borderwidth=1)
        label.pack(ipadx=1)
        # Auto close after 3 sec
        label.after(self._auto_close, self.close)

    def close(self, event=None):
        """
        Closes the tool tip (takes it down)
        :param event:
        :return:
        """
        if self._tw:
            self._tw.destroy()
            self._tw = None
