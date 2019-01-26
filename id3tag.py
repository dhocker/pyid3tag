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
# How to make an app
# https://py2app.readthedocs.io/en/latest/index.html
# https://www.metachris.com/2015/11/create-standalone-mac-os-x-applications-with-python-and-py2app/
#
# Icons
# https://stackoverflow.com/questions/12306223/how-to-manually-create-icns-files-using-iconutil
#

# Python 3
import os.path
from collections import OrderedDict
from tkinter import filedialog, messagebox
from tkinter import Tk, Frame, Button, Label, LabelFrame, Entry, StringVar
from tkinter import ttk
import tkinter
import mutagen
import mutagen.id3
import id3frames
from filelist_widget import FileList
from id3tags_widget import ID3TagsWidget
from status_bar import StatusBar


class ID3EditorFrame(Tk):
    def __init__(self):
        super(ID3EditorFrame, self).__init__()

        # Screen metrics
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        # Position and size main window
        self.title("ID3 Tag Editor")
        geo = "{0}x{1}+{2}+{3}".format(int(sw/2), int(sh/2), int(sw/8), int(sh/8))
        self.geometry(geo)
        self.resizable(width=True, height=True)

        self._filename = ""
        # TODO It would be nice to persist the last used path
        self._mp3_dir = "./"

        # ttk theme
        # s = ttk.Style()
        # s.theme_use('classic')
        self.background_color = "#ffffff"
        self.highlight_color = "#e0e0e0"

        # Create window widgets
        self._create_widgets(sw, sh)

        # Handle app exit
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_widgets(self, sw, sh):

        self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=2)

        # Left hand frame (file list)
        self._filelist = FileList(self, width=int(sw / 6) - 10, height=int(sh / 2) - 10,
                                  open=self._open_file, save=self._save_file)
        self._filelist.grid(row=0, column=0, sticky=tkinter.E + tkinter.W + tkinter.N +tkinter.S,
                            padx=10, pady=10)

        # Right hand frame (tags list)
        self._rhframe = Frame(self, width=int(sw / 6) - 20, height=100)
        self._rhframe.grid(row=0, column=1, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,
                           padx=10, pady=10)

        # Grid row tracker for right hand frame (tags info)
        gr = 0

        # Tags widget
        self._tags_frame = ID3TagsWidget(self._rhframe, text="Tags", width=int(sw / 4) - 10, height=10, borderwidth=2)
        self._tags_frame.grid(row=gr, column=0, sticky=tkinter.E + tkinter.W, padx=10)

        gr += 1

        # Footer frame
        self._footer_frame = Frame(self._rhframe, width=int(sw / 4) - 20, bg=self.highlight_color,
                                   bd=1, relief=tkinter.SOLID)
        self._footer_frame.grid(row=gr, column=0, sticky=tkinter.E + tkinter.W, padx=10, pady=10)

        # Status bar in footer frame
        self._status_bar = StatusBar(self._footer_frame, text="", bg=self.highlight_color, bd=0)
        self._status_bar.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

    def _on_close(self):
        """
        App is closing. Warn user if unsaved changes.
        :return:
        """
        if self._are_unsaved_changes():
            return False
        self.destroy()
        return True

    def _save_file(self, fn):
        self._tags_frame.commit_tag_updates()
        self.id3.save(fn)
        # messagebox.showinfo("Saved", "Tags saved to %s" % self.filename)
        # TODO How to handle this
        self._status_bar.set("Tags saved to %s" % fn)

    def _open_file(self, fn):
        # If unsaved changes were not handled, abort opening file
        if self._are_unsaved_changes():
            return

        # An existing mp3 file was selected, but there is
        # no guarantee that it contains an ID3 block.
        self.title("ID3 Tag Editor: " + fn)
        self._filename = fn
        # TODO It would be nice to persist the last used path
        self._mp3_dir = os.path.dirname(fn)

        # Load tags from file
        try:
            # self.mp3 = mutagen.mp3.MP3(fn)
            self.id3 = mutagen.id3.ID3(fn)
            self._tags_frame.load_tags(self.id3)
            self._status_bar.set(fn)
            self._tags_frame.tags_changed = False
        except mutagen.id3.ID3NoHeaderError as ex:
            messagebox.showerror("No Header Error", str(ex))
            self.id3 = mutagen.id3.ID3()
            self._tags_frame.load_tags(self.id3)
        except Exception as err:
            messagebox.showerror("Exception", str(err))

    def _are_unsaved_changes(self):
        """

        :return: True if changes have been handled. False if changes have not
        been handled.
        """
        if self._tags_frame.tags_changed:
            # askyesno returns True if YES was chosen.
            # Discard changes means there are no changes to save, so we return False
            return not messagebox.askyesno("Unsaved changes", "Discard changes?")
        return False


if __name__ == '__main__':
    main_frame = ID3EditorFrame()
    main_frame.mainloop()
    print (main_frame._filename)
    print("Ended")