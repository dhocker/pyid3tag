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
import re
import datetime
import tkinter as tk
import tkinter.ttk as ttk


class FileTreeView(tk.Frame):
    """
    File list in a TreeView widget
    """
    # TODO Add columns for size and date modified
    def __init__(self, parent, path,
                 width=100, height=100,
                 background=None,
                 select=None, action=None,
                 filter_regex=".+\.mp3$",
                 title="File TreeView"):
        """
        Create an instance of the widget
        :param parent: parent of this widget
        :param path: initial path for view
        :param width: Initial width in px
        :param height: Initial height in px
        :param background: Background color as a Tkinter color (e.g. "#e8e8e8") or None
        :param select: callback for item selection
        :param action: callback for double-click action
        :param filter_regex: filter regex for files (does not apply to directories)
        :param title: text for the title at the top of the widget
        """
        super(FileTreeView, self).__init__(parent)

        self._nodes = dict()
        self._title = title
        self._select_callback = select
        self._action_callback = action

        tree_style = ttk.Style()
        tree_style.theme_use("clam")
        if background:
            tree_style.configure("custom.Treeview", background=background, fieldbackground=background)
        tree_style.configure("custom.Treeview.Heading", font=(None, 12))
        tree_style.layout("custom.Treeview", [])

        # The TreeView widget and scroll bars
        # self._dir_tree = ttk.Treeview(self, show="tree headings", style="custom.Treeview")
        self._dir_tree = ttk.Treeview(self, show="tree headings", style="custom.Treeview")
        self._dir_tree.grid(row=0, column=0, sticky=tk.NSEW)
        ysb = ttk.Scrollbar(self, orient='vertical', command=self._dir_tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self._dir_tree.xview)
        self._dir_tree.configure(yscroll=ysb.set, xscroll=xsb.set)

        # Note that the columns definition does not include the icon column
        self._dir_tree["columns"] = ("Size", "Date Modified")
        self._dir_tree.column("#0", minwidth=300, stretch=True)
        self._dir_tree.column("Size", width=100, minwidth=100, stretch=False)
        self._dir_tree.column("Date Modified", width=0, minwidth=150)
        # Note that the file/dir name goes in the icon column
        self._dir_tree.heading('#0', text='Name', anchor='w')
        self._dir_tree.heading('Size', text='Size', anchor='w')
        self._dir_tree.heading('Date Modified', text='Date Modified', anchor='w')

        ysb.grid(row=0, column=1, sticky=tk.NS)
        xsb.grid(row=1, column=0, sticky=tk.EW)

        self._path = path
        # The filter is a regex expression that defaults to all mp3 files
        self.set_filter(filter_regex)

        # Event capture
        self._dir_tree.bind('<<TreeviewOpen>>', self._open_node)
        self._dir_tree.bind("<<TreeviewSelect>>", self._on_select)
        self._dir_tree.bind("<Double-1>", self._on_double_click)

    def _insert_node(self, parent, text, abspath):
        # Note that the tags value is used to hold the full filepath
        if os.path.isdir(abspath):
            values = ("",)
        else:
            # For a file, supply size and last modified time
            sr = os.lstat(abspath)
            sz = "{0:,}".format(sr.st_size)
            dt = datetime.datetime.fromtimestamp(sr.st_mtime)
            values = (sz, dt)
        # Here text is the icon column and values are the size and date columns
        node = self._dir_tree.insert(parent, 'end', open=False, tags=(abspath,),
                                     text=text, values=values)

        if os.path.isdir(abspath):
            self._nodes[node] = abspath
            self._dir_tree.insert(node, 'end')

    def _open_node(self, event):
        node = self._dir_tree.focus()
        abspath = self._nodes.pop(node, None)
        if abspath:
            self._dir_tree.delete(self._dir_tree.get_children(node))
            sorted_list = sorted(os.listdir(abspath), key=str.lower)
            for p in sorted_list:
                fullpath = os.path.join(abspath, p)
                # Filter contents (e.g. *.mp3 files)
                if (not os.path.isdir(fullpath)) and (not self._filter_regex.match(p)):
                    continue
                self._insert_node(node, p, fullpath)

    def _on_select(self, event):
        if self._select_callback:
            node = self._dir_tree.selection()
            # There seems to be no guarantee that something is selected
            if node:
                tags = self._dir_tree.item(node, "tags")
                if not os.path.isdir(tags[0]):
                    self._select_callback(tags[0])

    def _on_double_click(self, event):
        if self._action_callback:
            node = self._dir_tree.focus()
            filepath = self._dir_tree.item(node, "tags")
            if not os.path.isdir(filepath[0]):
                self._action_callback(filepath[0])

    def set_path(self, path):
        """
        Reset the file list to a new origin path
        :param path:
        :return:
        """
        self._dir_tree.delete(*self._dir_tree.get_children())
        abspath = os.path.abspath(path)
        self._insert_node('', abspath, abspath)
        self._path = path

    def set_filter(self, filter_regex):
        self._filter_regex = re.compile(filter_regex)
        self.set_path(self._path)


if __name__ == '__main__':
    """
    Test code
    """

    def action_handler(filepath):
        from tkinter import messagebox
        messagebox.showinfo("Action", filepath)

    root = tk.Tk()
    root.title("FileTreeView")

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    geo = "{0}x{1}".format(int(sw / 2), int(sh / 2))
    root.geometry(geo)
    # print(geo)

    # The FileTreeView widget is the only widget in the main window.
    # The main window and the FileTreeView are set up so the widget
    # resizes as the window is resized.

    # Make the main window resizable
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # The filter is for any mp3 file
    filter_regex=".+\.mp3$"
    title = "FileTreeView Example for mp3 Files (filter={0})".format(filter_regex)
    ftv = FileTreeView(root, path='.',
                       background="#e8e8e8",
                       action=action_handler, select=None,
                       filter_regex=filter_regex, title=title)
    ftv.grid(row=0, column=0, sticky=tk.NSEW)

    # Make the filetreeview resizable
    ftv.columnconfigure(0, weight=1)
    ftv.rowconfigure(0, weight=1)

    root.mainloop()
