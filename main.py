#!/usr/bin/env python3
"""
Short description of this Python module.
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
import subprocess
import os
import threading
import notify2

gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')  # Ensure you have the correct version
from gi.repository import Gtk, Vte, GLib, Gio

NOTIFY_SEND = 'notify-send '

class PackageManager:
    def __init__(self):
        
        self.icon_path = './icon/lazycat.png' or '/opt/lazycat/icon/lazycat.png'
        if not os.path.exists(self.icon_path):
            print('Error: Icon path not found')
            exit(1)

        notify2.init('lazyCat')

        self.window = Gtk.Window(title='lazyCat')
        self.window.set_icon_from_file(self.icon_path)
        self.window.connect('destroy', Gtk.main_quit)

        self.terminal = Vte.Terminal()
        self.terminal.set_font_scale(1.3)

        self.first_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.second_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.third_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        self.install_button = Gtk.Button(label='Install Package')
        self.install_button.connect('clicked', self.install_package)

        self.exec_label = Gtk.Label(label='Enter package name: ')
        self.exec_entry = Gtk.Entry()

        self.first_box.pack_start(self.terminal, True, True, 0)
        self.first_box.pack_end(self.second_box, False, False, 0)
        self.first_box.pack_end(self.third_box, False, False, 0)

        self.second_box.pack_end(self.install_button, True, True, 4)
        self.third_box.pack_start(self.exec_label, False, False, 4)
        self.third_box.pack_start(self.exec_entry, False, False, 4)

        self.window.add(self.first_box)

        self.spawn_terminal()

        self.window.show_all()

    def spawn_terminal(self):
        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.getenv('Home'),  # Working directory
            [os.environ.get('SHELL')],  # Command
            None,  # Environment
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,  # Child setup
            None,  # Child setup data
            -1,  # Timeout
            None,  # Cancellable
            self.child_ready  # Callback
        )

    def child_ready(self, terminal, pid, error, user_data):
        if not terminal or pid == -1:
            Gtk.main_quit()

    def install_package(self, widget):
        package_name = self.exec_entry.get_text().strip()
        if not package_name:
            notify2.Notification('Error', 'Please enter a package name').show()
            return

        install_command = f'pkexec apt install -y {package_name}'
        threading.Thread(target=self.run_installation, args=(install_command, package_name)).start()

    def run_installation(self, install_command, package_name):
        result = subprocess.run(install_command, shell=True, capture_output=True, text=True)
        GLib.idle_add(self.show_notification, result, package_name)

    def show_notification(self, result, package_name):
        if result.returncode == 0:
            notify2.Notification(f'{package_name} installed!', '').show()
        else:
            notify2.Notification('Error', 'Package not found').show()

if __name__ == '__main__':
    app = PackageManager()
    Gtk.main()
# V0.3: Python Script with Threading
