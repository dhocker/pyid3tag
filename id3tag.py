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

        # Handle changes to tag values
        self._tag_changed_event = (self.register(self._tag_changed_handler), '%d', '%V', '%W')
        self._tags_changed = False

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

        # Add tag button
        self._add_button = Button(self._buttons_frame, text="Add Tag", width=7, command=self._add_tag)
        self._add_button.grid(row=0, column=2, sticky=tkinter.W, padx=10)

        # Tag selection
        self._add_this_tag = StringVar()
        # Create list of available tags
        self._tag_list = ttk.Combobox(self._buttons_frame, values=id3frames.frame_keys(),
                                      width=6,
                                      textvariable=self._add_this_tag)
        self._tag_list.grid(row=0, column=3, sticky=tkinter.W)
        self._tag_list.state(['!disabled', 'readonly'])
        self._tag_list.current(0)

        # Delete tag button - deletes the current tag
        self._delete_button = Button(self._buttons_frame, text="Delete", width=6, command=self._delete_tag)
        self._delete_button.grid(row=0, column=4, sticky=tkinter.W, padx=10)

        gr += 1

        # Tags frame
        self._tags_frame = LabelFrame(self, text="Tags", width=int(sw / 3) - 20, height=100, borderwidth=2)
        self._tags_frame.grid(row=gr, column=0, sticky=tkinter.E + tkinter.W, padx=10)
        self.grid_columnconfigure(0, weight=1)
        # Each list item is a 2-tuple of tag label and tag text widget
        self._tag_widgets = []

        gr += 1

        # Footer frame
        self._footer_frame = Frame(self, width=int(sw / 3) - 20, bg=self.highlight_color, bd=1, relief=tkinter.SOLID)
        self._footer_frame.grid(row=gr, column=0, sticky=tkinter.E + tkinter.W, padx=10, pady=10)

        # Status bar in footer
        self._status_bar = Label(self._footer_frame, text="Status Bar", bg=self.highlight_color)
        self._status_bar.grid(row=0, column=0, sticky=tkinter.W)

    def _on_close(self):
        """
        App is closing. Warn user if unsaved changes.
        :return:
        """
        if self._tags_changed:
            if not messagebox.askyesno("Unsaved changes", "Discard changes?"):
                return False
        self.destroy()
        return True

    def _add_tag(self):
        t = self._add_this_tag.get()
        f = id3frames.create(t, "")
        self.id3.add(f)
        self._tags_changed = True
        # Reload all of the tags so they are sorted
        self._load_tags(self.id3)

    def _delete_tag(self):
        messagebox.showinfo("Delete", "Not implemented")

    def _save_file(self):
        self._commit_tag_updates()
        self.id3.save(self._filename)
        # messagebox.showinfo("Saved", "Tags saved to %s" % self.filename)
        self._status_bar["text"] = "Tags saved to %s" % self._filename
        self._tags_changed = False

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
                self._load_tags(self.id3)
            except mutagen.id3.ID3NoHeaderError as ex:
                messagebox.showerror("No Header Error", str(ex))
                self.id3 = mutagen.id3.ID3()
            except Exception as err:
                messagebox.showerror("Exception", str(err))

    def _load_tags(self, id3):
        # Delete existing tags
        for t in self._tag_widgets:
            t[0].destroy()
            t[1].destroy()
        self._tag_widgets = []

        # Sort tags
        sorted_tags = OrderedDict(sorted(id3.items()))

        for tag in sorted_tags:
            # Tags we don't support or handle
            tag4 = tag.upper()[0:4]
            if tag4 in ["APIC", "PRIV"]:
                continue

            # Tag name and value widgets
            self._add_tag_widget(tag, id3[tag].text[0])

        self._tags_frame.grid_columnconfigure(0, weight=1)
        self._tags_frame.grid_columnconfigure(1, weight=4)

    def _add_tag_widget(self, tag, value):
        # Determine the grid row for this tag
        gr = len(self._tag_widgets)

        # Tag name widget
        v = StringVar(value=tag)
        tw = Label(self._tags_frame, textvariable=v)
        tw.value_var = v
        tw.grid(row=gr, column=0, sticky=tkinter.E)

        tw.tooltip = id3frames.frame_tooltip(tag)
        tw.bind("<Enter>", self._on_enter_tag)
        tw.bind("<Leave>", self._on_leave_tag)

        # Tag value widget
        v = StringVar(value=value)
        # w = max(50, len(v.get()))
        tvw = Entry(self._tags_frame, textvariable=v, validate='key',
                    validatecommand=self._tag_changed_event)
        tvw.value_var = v
        tvw.grid(row=gr, column=1, sticky=tkinter.W + tkinter.E)

        tvw.tooltip = id3frames.frame_tooltip(tag)
        tvw.label_widget = tw
        tvw.tag_name = tag
        tvw.bind("<Enter>", self._on_enter_tag)
        tvw.bind("<Leave>", self._on_leave_tag)
        tvw.bind("<FocusIn>", self._on_focusin)
        tvw.bind("<FocusOut>", self._on_focusout)

        self._tag_widgets.append((tw, tvw))

    def _on_enter_tag(self, event):
        self._status_bar["text"] = event.widget.tooltip

    def _on_leave_tag(self, event):
        self._status_bar["text"] = ""

    def _on_focusin(self, event):
        event.widget.label_widget["bg"] = self.highlight_color

    def _on_focusout(self, event):
        tvw = event.widget
        tvw.label_widget["bg"] = self.background_color
        # Save edited tag value
        self._update_tag(tvw.tag_name, tvw.value_var.get())

    def _commit_tag_updates(self):
        for t in self._tag_widgets:
            # t[0] is the tag label widget and t[1] is its value widget
            # f = mutagen.id3.Frames[t[0].value_var.get()](text=t[1].value_var.get())
            # f = mutagen.id3.Frame(t[0].value_var.get(), text=t[1].value_var.get())
            tag_name = t[1].tag_name
            tag_value = t[1].value_var.get()

            self._update_tag(tag_name, tag_value)

    def _update_tag(self, name, value):
        f = id3frames.create(name, value)
        if f:
            self.id3.add(f)
        else:
            # Skip tags without a creator
            pass

    def _tag_changed_handler(self, action_code, reason, name):
        """
        Track changes to tag values
        :param action_code:
        :param reason:
        :param name:
        :return:
        """
        # How to find the actual widget that has changed
        for t in self._tag_widgets:
            if str(t[1]) == name:
                # print("Named entry widget found")
                break

        # print("Tag changed event: <{0}><{1}><{2}>".format(action_code, reason, name))
        if reason == 'key' and action_code in ['0', '1']:
            self._tags_changed = True
        return True


if __name__ == '__main__':
    main_frame = ID3EditorFrame()
    main_frame.mainloop()
    print (main_frame._filename)
    print("Ended")