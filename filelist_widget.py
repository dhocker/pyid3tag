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

import os
from tkinter import Button, Frame, LabelFrame, Listbox, filedialog, Scrollbar
import tkinter
from status_bar import StatusBar


class FileList(Frame):
    """
    File list widget with vertical and horizontal scrollbars
    """

    def __init__(self, parent, width=100, height=100, borderwidth=0, open=None, save=None):
        super(FileList, self).__init__(parent, width=width, height=height,
                                       borderwidth=borderwidth)

        self._save_file_callback = save
        self._open_file_callback = open
        self._file_type = None
        # TODO It would be nice to persist the last used path
        self._mp3_dir = "./"

        self.background_color = "#ffffff"
        self.highlight_color = "#e0e0e0"

        # create widgets

        # Header/buttons frame
        self._buttons_frame = Frame(self, width=width, height=10)
        self._buttons_frame.grid(row=0, column=0, sticky=tkinter.E + tkinter.W, padx=10, pady=10)

        # Open Directory button
        self._open_button = Button(self._buttons_frame, text="Directory", width=10, command=self._open_directory)
        self._open_button.grid(row=0, column=0, sticky=tkinter.W, padx=2)

        # Open File button
        self._open_button = Button(self._buttons_frame, text="File", width=5, command=self._open_file)
        self._open_button.grid(row=0, column=1, sticky=tkinter.W, padx=2)

        # Save file button
        self._save_button = Button(self._buttons_frame, text="Save", width=5, command=self._save_file)
        self._save_button.grid(row=0, column=2, sticky=tkinter.W, padx=2)

        # Vertical scrollbar
        self._filelist_vscroll = Scrollbar(self, orient=tkinter.VERTICAL)
        self._filelist_vscroll.grid(row=1, column=1, sticky=tkinter.N + tkinter.S)

        # Horizontal scrollbar
        self._filelist_hscroll = Scrollbar(self, orient=tkinter.HORIZONTAL)
        self._filelist_hscroll.grid(row=2, column=0, sticky=tkinter.W + tkinter.E)

        # File list
        self._filelist = Listbox(self, width=int(width / 10), height=int(height / 20) - 2,
                                 selectmode=tkinter.SINGLE,
                                 xscrollcommand=self._filelist_hscroll.set,
                                 yscrollcommand=self._filelist_vscroll.set)
        self._filelist.grid(row=1, column=0,
                            sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,
                            padx=10, pady=10)
        self._filelist_hscroll['command'] = self._filelist.xview
        self._filelist_vscroll['command'] = self._filelist.yview
        self._filelist.bind("<Double-1>", self._open_file)

        # Status bar in footer frame
        self._status_bar = StatusBar(self, text="", bg=self.highlight_color, bd=1)
        self._status_bar.grid(row=3, column=0, sticky=tkinter.W + tkinter.E)

    def _save_file(self):
        if self._save_file_callback:
            self._save_file_callback(self._mp3_dir + self._filename)

    def _open_directory(self):
        # TODO Change to open directory
        directory = filedialog.askdirectory(initialdir=self._mp3_dir, title="Select directory")
        if directory:
            if not directory.endswith("/"):
                directory += "/"
            self._mp3_dir = directory
           # Load listbox with files from directory
            self._filelist.delete(0, last=self._filelist.size() - 1)
            for file in os.listdir(directory):
                if file.endswith(".mp3"):
                    self._filelist.insert(tkinter.END, file)
            self._status_bar.set(directory)

    def _open_file(self, *args):
        selectedx = self._filelist.curselection()[0]
        selected = self._filelist.get(selectedx)
        self._filename = selected

        if self._open_file_callback:
            self._open_file_callback(self._mp3_dir + selected)
