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

from tkinter import Label, StringVar
import tkinter


class StatusBar(Label):
    def __init__(self, parent, text="", bg=None, bd=2, relief=tkinter.SOLID):
        self._status_var = StringVar(value=text)
        super(StatusBar, self).__init__(parent, textvariable=self._status_var, bg=bg, bd=bd, relief=relief)

    def set(self, text):
        self._status_var.set(text)

    def get(self):
        self._status_var.get()