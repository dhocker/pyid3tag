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

from collections import OrderedDict
from tkinter import filedialog, messagebox
from tkinter import Tk, Frame, Button, Label, LabelFrame, Entry, StringVar, OptionMenu, \
    simpledialog
import tkinter
import id3frames
from tool_tip_popup import ToolTipPopup
from tag_help_window import TagHelpWindow


class ID3TagsWidget(LabelFrame):
    def __init__(self, parent, text="", width=100, height=10, borderwidth=0,
                 tag_changed=None):
        super(ID3TagsWidget, self).__init__(parent, text=text, width=width, height=height,
                                            borderwidth=borderwidth)

        self.background_color = "#ffffff"
        self.highlight_color = "#e0e0e0"
        self.id3 = None
        self._tags_changed = False
        self._tag_changed_callback = tag_changed
        self._tag_help_window = None

        # Each list item is a 2-tuple of tag label and tag text widget
        self._tag_widgets = []
        self._selected_tag = None

        # Header/buttons frame
        self._buttons_frame = Frame(self, width=int(width / 3) - 20, height=10)
        self._buttons_frame.grid(row=0, column=0, sticky=tkinter.E + tkinter.W, padx=10, pady=10)
        self._buttons_frame.columnconfigure(0, weight=1)

        # Add tag button
        self._add_button = Button(self._buttons_frame, text="Add Tag", width=7, command=self._add_tag)
        self._add_button.grid(row=0, column=1, sticky=tkinter.E, padx=10)

        # Tag selection as an OptionMenu
        self._add_this_tag = StringVar()
        opts = id3frames.frame_keys()
        self._add_this_tag.set(opts[0])
        self._tag_opt = OptionMenu(self._buttons_frame, self._add_this_tag, *opts)
        self._tag_opt.config(width=10)
        self._tag_opt.grid(row=0, column=2, sticky=tkinter.E, padx=10)

        # Tag help button
        self._tag_help_button = Button(self._buttons_frame, text="Tag Help", width=9, command=self.show_tag_help)
        self._tag_help_button.grid(row=0, column=3, sticky=tkinter.E, padx=10)

        # Delete tag button - deletes the current tag
        self._delete_button = Button(self._buttons_frame, text="Delete Tag", width=10,
                                     command=self._delete_tag, state=tkinter.DISABLED)
        self._delete_button.grid(row=0, column=4, sticky=tkinter.E, padx=10)

        # Handle changes to tag values
        self._tag_changed_event = (self.register(self._tag_changed_handler), '%d', '%V', '%W')

        # Tags frame
        self._tags_frame = Frame(self, width=width - 20, height=height, borderwidth=2)
        self._tags_frame.grid(row=1, column=0, sticky=tkinter.E + tkinter.W, padx=10)

        self._tags_frame.columnconfigure(0, weight=1)
        # self._tags_frame.columnconfigure(1, weight=4)

        self.columnconfigure(0, weight=1)

    @property
    def tags_changed(self):
        return self._tags_changed

    @tags_changed.setter
    def tags_changed(self, value):
        self._tags_changed = value

    def add_tag(self, tag):
        if tag == "COMM":
            # Get description and language
            comm_parms = self._get_comm_tag_parms()
            if not comm_parms:
                return
            tag = tag + ":" + comm_parms
        f = id3frames.create(tag, "?")
        self.id3.add(f)
        self._tags_changed = True
        # Reload all of the tags so they are sorted
        self.load_tags(self.id3)

        if self._tag_changed_callback:
            self._tag_changed_callback(tag, "")

    def _get_comm_tag_parms(self):
        """
        Get description and language
        :return:
        """
        valid = False
        while not valid:
            comm_parms = simpledialog.askstring("COMM Description and Language",
                                                "Enter description:XXX where XXX is a 3 letter language")
            if not comm_parms:
                return None

            parts = comm_parms.split(':')
            if len(parts) != 2 or len(parts[1]) != 3:
                messagebox.showerror("COMM Description:Language", "Required format is description:XXX\nWhere XXX is a 3 character language identifier")
            else:
                valid = True
        return comm_parms

    def load_tags(self, id3):
        self.id3 = id3
        # Delete existing tags
        for t in self._tag_widgets:
            t[0].destroy()
            t[1].destroy()

        # Brute force way to get the tags frame resized
        self._tags_frame.grid_remove()
        self._tags_frame.grid()

        self._tag_widgets = []

        # Sort tags
        sorted_tags = OrderedDict(sorted(id3.items()))

        for tag in sorted_tags:
            # Tags we don't support or handle
            tag4 = tag.upper()[0:4]
            # Handle unsupported tags better
            if tag4 in id3frames.frame_keys():
                # Tag name and value widgets
                self._add_supported_tag(tag, id3[tag].text[0])
            else:
                self._add_unsupported_tag(tag)

    def _add_supported_tag(self, tag, value):
        # Determine the grid row for this tag
        gr = len(self._tag_widgets)

        # Tag name widget
        tw = self._add_tag_name_label(gr, tag)

        # Tag value widget
        v = StringVar(value=value)
        w = max(30, len(v.get()))
        tvw = Entry(self._tags_frame, textvariable=v, validate='key',
                    validatecommand=self._tag_changed_event,
                    width=w)
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

    def _add_unsupported_tag(self, tag):
        # Determine the grid row for this tag
        gr = len(self._tag_widgets)

        # Tag name widget
        # Some unsupported tags can be very long
        if len(tag) > 30:
            tag = tag[:4] + "[length={0}]".format(len(tag))
        tw = self._add_tag_name_label(gr, tag)

        # Place holder tag value widget
        v = StringVar(value="Unsupported")
        w = max(30, len(v.get()))
        tvw = Label(self._tags_frame, textvariable=v, width=w, anchor=tkinter.W)
        tvw.value_var = v
        tvw.grid(row=gr, column=1, sticky=tkinter.W)

        tvw.tooltip = id3frames.frame_tooltip(tag)
        tvw.label_widget = tw
        tvw.tag_name = tag
        # tvw.bind("<Enter>", self._on_enter_tag)
        # tvw.bind("<Leave>", self._on_leave_tag)
        # tvw.bind("<FocusIn>", self._on_focusin)
        # tvw.bind("<FocusOut>", self._on_focusout)

        self._tag_widgets.append((tw, tvw))

    def _add_tag_name_label(self, gr, tag):
        # Tag name widget
        v = StringVar(value=tag)
        tw = Label(self._tags_frame, textvariable=v)
        tw.value_var = v
        tw.grid(row=gr, column=0, sticky=tkinter.E)

        tw.tooltip = ToolTipPopup(tw, id3frames.frame_tooltip(tag[:4]))

        return tw

    def _add_tag(self):
        t = self._add_this_tag.get()
        self.add_tag(t)

    def show_tag_help(self):
        if not self._tag_help_window:
            # Position the help window to the right of the main window
            top = self.winfo_toplevel()
            self._tag_help_window = TagHelpWindow(self,
                                                  x=top.winfo_rootx() + top.winfo_width() + 1,
                                                  y=top.winfo_rooty(),
                                                  width=400, height=200,
                                                  close=self._on_tag_help_close)
        else:
            self._tag_help_window.show()

    def _on_tag_help_close(self):
        """
        The help window was closed.
        :return:
        """
        self._tag_help_window = None
        return True

    def _delete_tag(self):
        # Need to know the currently selected tag
        tag_name = self._selected_tag.label_widget.value_var.get()
        self.id3.delall(tag_name)
        # Need to update tags list
        self.load_tags(self.id3)
        self.tags_changed = True
        if self._tag_changed_callback:
            self._tag_changed_callback(tag_name, None)

    def _on_enter_tag(self, event):
        pass

    def _on_leave_tag(self, event):
        pass

    def _on_focusin(self, event):
        event.widget.label_widget["bg"] = self.highlight_color
        self._selected_tag = event.widget
        self._delete_button.configure(state=tkinter.NORMAL)

    def _on_focusout(self, event):
        tvw = event.widget
        tvw.label_widget["bg"] = self.background_color
        # Save edited tag value
        self._update_tag(tvw.tag_name, tvw.value_var.get())
        self._delete_button.configure(state=tkinter.DISABLED)

    def commit_tag_updates(self):
        # TODO Is this needed now that on_focusout also saves the tag value?
        for t in self._tag_widgets:
            # t[0] is the tag label widget and t[1] is its value widget
            # f = mutagen.id3.Frames[t[0].value_var.get()](text=t[1].value_var.get())
            # f = mutagen.id3.Frame(t[0].value_var.get(), text=t[1].value_var.get())
            tag_name = t[1].tag_name
            tag_value = t[1].value_var.get()

            self._update_tag(tag_name, tag_value)

        self._tags_changed = False

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
                changed = t
                break

        # print("Tag changed event: <{0}><{1}><{2}>".format(action_code, reason, name))
        if reason == 'key' and action_code in ['0', '1']:
            self._tags_changed = True
            changed_tag = changed[0].value_var.get()
            new_value = changed[1].value_var.get()
            if self._tag_changed_callback:
                self._tag_changed_callback(changed_tag, new_value)
        return True
