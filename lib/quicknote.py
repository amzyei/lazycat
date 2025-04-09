#!/usr/bin/python3

""" 

Short description of this python3 module.
Longer description of this module.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
[AMZYEI]
"""


import gi
import os
import uuid
from datetime import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import notify2

class QuickNoteWindow(Gtk.Window):
    def __init__(self, quick_note):
        super().__init__(title="Quick Note")
        self.quick_note = quick_note
        self.set_default_size(300, 200)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_transient_for(quick_note.parent)  # Set the parent window

        self.note_entry = Gtk.TextView()
        self.note_entry.set_wrap_mode(Gtk.WrapMode.WORD)

        self.save_button = Gtk.Button(label="Save Note")
        self.save_button.connect("clicked", self.on_save_button_clicked)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.vbox.pack_start(self.note_entry, True, True, 0)
        self.vbox.pack_start(self.save_button, False, False, 0)

        self.add(self.vbox)

    def on_save_button_clicked(self, widget):
        buffer = self.note_entry.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        note = buffer.get_text(start_iter, end_iter, True)
        self.quick_note.save_note(note)
        self.destroy()

class QuickNote:
    def __init__(self, parent):
        self.parent = parent
        notify2.init('LazyCat')

    def show(self):
        QuickNoteWindow(self).show_all()

    def save_note(self, note):
        # Generate a unique filename
        note_start = note[:20].replace(' ', '_')  # Take the first 20 characters and replace spaces with underscores
        note_uuid = uuid.uuid4()
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{note_start}_{note_uuid}_{current_time}.txt"
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', filename)

        # Save the note to the desktop
        with open(desktop_path, 'w') as file:
            file.write(note)

        # Show a notification
        notify2.Notification('Note Saved', f"Note saved to: {desktop_path}").show()
