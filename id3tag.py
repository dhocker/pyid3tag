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
        geo = "{0}x{1}+{2}+{3}".format(int(sw/3), int(sh/2), int(sw/8), int(sh/8))
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
        # Grid row tracker
        gr = 0

        # Header/buttons frame
        self._buttons_frame = Frame(self, width=int(sw / 3) - 20, height=100)
        self._buttons_frame.grid(row=gr, column=0, sticky=tkinter.E + tkinter.W, padx=10, pady=10)

        # Open File button
        self._open_button = Button(self._buttons_frame, text="Open", width=6, command=self._open_file)
        self._open_button.grid(row=0, column=0, sticky=tkinter.W, padx=10)

        # Save file button
        self._save_button = Button(self._buttons_frame, text="Save", width=6, command=self._save_file)
        self._save_button.grid(row=0, column=1, sticky=tkinter.W, padx=10)

        gr += 1

        # Tags widget
        self._tags_frame = ID3TagsWidget(self, text="Tags", width=int(sw / 3) - 20, height=10, borderwidth=2)
        self._tags_frame.grid(row=gr, column=0, sticky=tkinter.E + tkinter.W, padx=10)
        self.grid_columnconfigure(0, weight=1)

        gr += 1

        # Footer frame
        self._footer_frame = Frame(self, width=int(sw / 3) - 20, bg=self.highlight_color, bd=1, relief=tkinter.SOLID)
        self._footer_frame.grid(row=gr, column=0, sticky=tkinter.E + tkinter.W, padx=10, pady=10)

        # Status bar in footer frame
        self._status_bar = StatusBar(self._footer_frame, text="Status Bar", bg=self.highlight_color)
        self._status_bar.grid(row=0, column=0, sticky=tkinter.W)

    def _on_close(self):
        """
        App is closing. Warn user if unsaved changes.
        :return:
        """
        if self._tags_frame.tags_changed:
            if not messagebox.askyesno("Unsaved changes", "Discard changes?"):
                return False
        self.destroy()
        return True

    def _save_file(self):
        self._tags_frame.commit_tag_updates()
        self.id3.save(self._filename)
        # messagebox.showinfo("Saved", "Tags saved to %s" % self.filename)
        # TODO How to handle this
        self._status_bar.set("Tags saved to %s" % self._filename)

    def _open_file(self):
        fn = filedialog.askopenfilename(initialdir=self._mp3_dir, title="Select file",
                                        filetypes=(("mp3 files", "*.mp3"),("all files", "*.*")))
        if fn:
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
            except mutagen.id3.ID3NoHeaderError as ex:
                messagebox.showerror("No Header Error", str(ex))
                self.id3 = mutagen.id3.ID3()
                self._tags_frame.load_tags(self.id3)
            except Exception as err:
                messagebox.showerror("Exception", str(err))


if __name__ == '__main__':
    main_frame = ID3EditorFrame()
    main_frame.mainloop()
    print (main_frame._filename)
    print("Ended")