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
import inspect
from collections import OrderedDict
from tkinter import filedialog, messagebox
from tkinter import Tk, Frame, Button, Label, LabelFrame, Entry, StringVar, Menu, PanedWindow
from tkinter import ttk
import tkinter
import mutagen
import mutagen.id3
import id3frames
from filelist_widget import FileList
from filetreeview import FileTreeView
from id3tags_widget import ID3TagsWidget
from status_bar import StatusBar
from text_message_box import TextMessageBox


class ID3EditorApp(Tk):
    def __init__(self):
        super(ID3EditorApp, self).__init__()

        # Screen metrics
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        # Position and size main window
        self.title("ID3 Tag Editor")
        geo = "{0}x{1}+{2}+{3}".format(int(sw/2), int(sh/2), int(sw/8), int(sh/8))
        self.geometry(geo)
        self.resizable(width=True, height=True)

        # The currently opened file
        self._filename = ""
        # The currently selected file (may not be open)
        self._selected_filename = ""
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
        # will return x11 (Linux), win32 or aqua (macOS)
        gfx_platform = self.tk.call('tk', 'windowingsystem')

        # App menu bar
        self._menu_bar = Menu(self)

        # macOS app menu covering things specific to macOS X
        if gfx_platform == "aqua":
            self._appmenu = Menu(self._menu_bar, name='apple')
            self._appmenu.add_command(label='About pyid3tag', command=self._show_about)
            self._appmenu.add_separator()
            self._menu_bar.add_cascade(menu=self._appmenu, label='pyid3tag')

            self.createcommand('tk::mac::ShowPreferences', self._show_preferences)

        # File menu
        self._file_menu = Menu(self._menu_bar, tearoff=0)
        self._file_menu.add_command(label="Open directory", command=self._open_directory_command)
        self._file_menu.add_command(label="Edit file", command=self._open_file_command,
                                    state=tkinter.DISABLED)
        self._file_menu_edit_index = 1
        self._file_menu.add_command(label="Save file", command=self._save_file_command, state=tkinter.DISABLED)
        self._file_menu_save_index = 2
        self._file_menu.add_separator()
        self._file_menu.add_command(label="Quit", command=self._on_close)
        self._menu_bar.add_cascade(label="File", menu=self._file_menu)

        # Help menu
        self._help_menu = Menu(self._menu_bar, tearoff=0)
        # Linux or Win
        # Reference: https://tkdocs.com/tutorial/menus.html
        if gfx_platform != 'aqua':
            self._help_menu.add_command(label="About", command=self._show_about)
        self._help_menu.add_command(label="Application", command=self._show_app_help)
        self._help_menu.add_command(label="Tags", command=self._show_tag_help)
        self._menu_bar.add_cascade(label="Help", menu=self._help_menu)

        self.config(menu=self._menu_bar)

        # paned window - this is the only child of the app window
        self._paned = PanedWindow(self, orient=tkinter.HORIZONTAL,
                                  showhandle=True, handlesize=16,
                                  sashwidth=20, sashrelief=tkinter.SUNKEN)
        # self._paned.grid(row=0, column=0, sticky=tkinter.NSEW)
        self._paned.pack(fill=tkinter.BOTH, expand=1)

        # Left hand frame (file list)
        self._filelist = FileTreeView(self._paned, ".",
                                      background=None,
                                      action=self._open_file,
                                      select=self._select_file)

        # Make the filetreeview resizable
        self._filelist.columnconfigure(0, weight=1)
        self._filelist.rowconfigure(0, weight=1)

        # Right hand frame (tags list)
        self._rhframe = Frame(self._paned)

        # Grid row tracker for right hand frame (tags info)
        gr = 0

        # Tags widget
        self._tags_frame = ID3TagsWidget(self._rhframe, text="Tags", width=int(sw / 4) - 10,
                                         height=10, borderwidth=2,
                                         tag_changed=self._changed_tag)
        self._tags_frame.grid(row=gr, column=0, sticky=tkinter.NSEW, padx=10)

        gr += 1

        # Footer frame
        # TODO Refactor this code to the "tags widget"
        self._footer_frame = Frame(self._rhframe, width=int(sw / 4) - 20, bg=self.highlight_color,
                                   bd=1, relief=tkinter.SOLID)
        self._footer_frame.grid(row=gr, column=0, sticky=tkinter.EW, padx=10, pady=10)

        # Status bar in footer frame
        self._status_bar = StatusBar(self._footer_frame, text="", bg=self.highlight_color, bd=0)
        self._status_bar.grid(row=0, column=0, sticky=tkinter.EW)

        # This is the key to getting both panes to expand equally
        # Ref: https://stackoverflow.com/questions/27636904/how-to-create-expanding-panedwindow-with-gridlayout-in-tkinter
        self._paned.add(self._filelist, stretch="always")
        self._paned.add(self._rhframe, stretch="always")

    def _show_preferences(self):
        tkinter.messagebox.showinfo("Preferences for pyid3tag", "None currently defined")

    def _show_about(self):
        about_text = \
            "Copyright © 2019 by Dave Hocker\n" + \
            "\n" + \
            "Source: https://github.com/dhocker/pyid3tag\n" + \
            "License: GNU General Public License v3\n" + \
            "as published by the Free Software Foundation, Inc."

        # Locate logo image file
        cwd = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
        if os.path.exists(cwd + "/id3tag.gif"):
            image_path = cwd + "/id3tag.gif"
        elif os.path.exists(cwd + "/resources/id3tag.gif"):
            image_path = cwd + "/resources/id3tag.gif"
        else:
            image_path = "id3tag.gif"

        # This is a modal message box
        mb = TextMessageBox(self, title="About pyid3tag", text=about_text,
                            heading="ID3 Tag Editor",
                            image=image_path, orient=tkinter.HORIZONTAL)
        mb.show()
        self.wait_window(window=mb)

    def _show_app_help(self):
        import webbrowser
        webbrowser.open("https://github.com/dhocker/pyid3tag/blob/master/README.md", new=2)

    def _show_tag_help(self):
        self._tags_frame.show_tag_help()

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
        """
        Save the current tags into its file
        :param fn: File where tags are to be saved
        :return: None
        """
        self._tags_frame.commit_tag_updates()
        self.id3.save(fn)
        self._file_menu.entryconfigure(self._file_menu_save_index, state=tkinter.DISABLED)
        self._status_bar.set("Tags saved to %s" % fn)

    def _open_file(self, fn):
        # If unsaved changes were not handled, abort opening file
        if self._are_unsaved_changes():
            return

        # An existing mp3 file was selected, but there is
        # no guarantee that it contains an ID3 block.
        self.title("ID3 Tag Editor: " + fn)
        # Remember where the tags came from
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
            self._file_menu.entryconfigure(self._file_menu_save_index, state=tkinter.DISABLED)
        except mutagen.id3.ID3NoHeaderError as ex:
            # messagebox.showerror("No Header Error", str(ex))
            self._status_bar.set(str(ex))
            self.id3 = mutagen.id3.ID3()
            self._tags_frame.load_tags(self.id3)
        except Exception as err:
            messagebox.showerror("Exception", str(err))

    def _select_file(self, fn):
        """
        A file has been selected.
        :param fn: Full path of selected file.
        :return: None
        """
        # Once a file is selected it can be opened
        self._selected_filename = fn
        self._file_menu.entryconfigure(self._file_menu_edit_index, state=tkinter.NORMAL)

    def _open_directory(self):
        """
        A new directory has been opened.
        :return:
        """
        # Since nothing is selected, disable the open file menu item
        self._file_menu.entryconfigure(self._file_menu_edit_index, state=tkinter.DISABLED)

    def _open_directory_command(self):
        directory = filedialog.askdirectory(initialdir=self._mp3_dir, title="Select directory")
        if directory:
            self._filelist.set_path(directory)
            # Since nothing is selected, disable the open file menu item
            self._file_menu.entryconfigure(self._file_menu_edit_index, state=tkinter.DISABLED)

    def _open_file_command(self):
        self._open_file(self._selected_filename)

    def _save_file_command(self):
        self._save_file(self._filename)

    def _changed_tag(self, tag_name, tag_value):
        self._file_menu.entryconfigure(self._file_menu_save_index, state=tkinter.NORMAL)
        # TODO How to pass changed_tag event to filelist widget?

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
    main_frame = ID3EditorApp()
    main_frame.mainloop()
