#!/usr/bin/python3

"""
Short description of this Python3 module.
Longer description of this module.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
[AMZYEI]
"""

import sys
import os
import notify2
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib

from lib import clockbar
from lib import quicknote


class LazyCat:
    """
    LazyCat is a simple GTK application that provides a terminal and a quick note feature.
    """

    def __init__(self):
        """
        Initializes the LazyCat application.
        """
        self.icon_path = './icon/lazycat.png' if os.path.exists('./icon/lazycat.png') else '/opt/lazycat/icon/lazycat.png'
        if not os.path.exists(self.icon_path):
            notify2.Notification('Error', 'Icon path not found').show()
            sys.exit(1)

        self.window = Gtk.Window(title='lazyCat')
        self.window.set_icon_from_file(self.icon_path)
        self.window.connect('destroy', Gtk.main_quit)

        self.terminal = Vte.Terminal()
        self.terminal.set_font_scale(1.3)
        self.terminal.connect('child-exited', self.on_child_exited)

        self.clock = clockbar.Clock(self.window)  # Initialize the clock

        self.quick_note_button = Gtk.Button(label='Quick Note')
        self.quick_note_button.connect('clicked', self.on_quick_note_button_clicked)

        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.pack_end(self.quick_note_button)

        self.window.set_titlebar(self.header_bar)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.vbox.pack_start(self.terminal, True, True, 0)

        self.window.add(self.vbox)

        self.spawn_terminal()

        self.quick_note = quicknote.QuickNote(self.window)  # Initialize the QuickNote instance with the window

        self.window.show_all()

    def spawn_terminal(self):
        """
        Spawns a new terminal.
        """
        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.path.expanduser('~'),
            [os.environ.get('SHELL', '/bin/sh')],
            None,
            GLib.SpawnFlags.SEARCH_PATH,
            None,
            None,
            -1,
            None,
            self.child_ready,
            None  # Pass None for user_data
        )

    def child_ready(self, terminal, pid, error=None, user_data=None):
        """
        Handles the child process being ready.
        """
        if not terminal or pid == -1:
            notify2.Notification('Error', 'Failed to spawn terminal').show()
            Gtk.main_quit()

    def on_child_exited(self, terminal, status):
        """
        Handles the terminal child process exiting.
        """
        if status == 9:
            notify2.Notification('FORCE',  'Force Quit').show()

        elif status != 0:
            notify2.Notification('Error', f'Terminal exited with an error code: {status}').show()
        else:
            Gtk.main_quit()

    def on_quick_note_button_clicked(self, widget):
        """
        Handles the quick note button click event.
        """
        self.quick_note.show()

def main():
    """
    Main function to initialize and run the LazyCat application.
    """
    app = LazyCat()
    Gtk.main()

if __name__ == '__main__':
    main()
