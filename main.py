#!/usr/bin/python3                                                            
                                                                              
"""                                                                           
                                                                              
Short description of this python3 module.                                     
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
import subprocess
import threading
import notify2
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib

from lib import clockbar


class LazyCat:
    """
    LazyCat is a simple GTK application that provides a terminal and a button to install packages.
    """

    def __init__(self):
        """
        Initializes the LazyCat application.
        """
        self.icon_path = './icon/lazycat.png' if  os.system('./icon/lazycat.png') == 0  else '/opt/lazycat/icon/lazycat.png'
        if not os.path.exists(self.icon_path):
            notify2.Notification('Error', 'Icon path not found').show()
            sys.exit(1)

        notify2.init('lazyCat')

        self.window = Gtk.Window(title='lazyCat')
        self.window.set_icon_from_file(self.icon_path)
        self.window.connect('destroy', Gtk.main_quit)

        self.terminal = Vte.Terminal()
        self.terminal.set_font_scale(1.3)
        self.terminal.connect('child-exited', self.on_child_exited)

        self.install_button = Gtk.Button(label='Install Package')
        self.install_button.connect('clicked', self.on_install_button_clicked)

        self.exec_label = Gtk.Label(label='Enter package name: ')
        self.exec_entry = Gtk.Entry()

        self.clock = clockbar.Clock(self.window)  # Initialize the clock

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        self.vbox.pack_start(self.terminal, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)

        self.hbox.pack_start(self.exec_label, False, False, 0)
        self.hbox.pack_start(self.exec_entry, True, True, 0)
        self.hbox.pack_start(self.install_button, False, False, 0)

        self.window.add(self.vbox)

        self.spawn_terminal()

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
        if status != 0:
            notify2.Notification('Error', 'Terminal exited with an error').show()
        else:
            Gtk.main_quit()            

    def on_install_button_clicked(self, widget):
        """
        Handles the install button click event.
        """
        package_name = self.exec_entry.get_text().strip()
        if not package_name:
            notify2.Notification('Error', 'Please enter a package name').show()
            return

        install_command = f'pkexec apt install -y {package_name}'
        threading.Thread(target=self.run_installation, args=(install_command, package_name)).start()

    def run_installation(self, install_command, package_name):
        """
        Runs the package installation command.
        """
        try:
            result = subprocess.run(install_command, shell=True, capture_output=True, text=True, check=True)
            GLib.idle_add(self.show_notification, result, package_name)
        except subprocess.CalledProcessError as e:
            GLib.idle_add(self.show_notification, e, package_name)

    def show_notification(self, result, package_name):
        """
        Shows a notification for the installation result.
        """
        if isinstance(result, subprocess.CalledProcessError):
            notify2.Notification('Error', f'Failed to install {package_name}.').show()
        else:
            notify2.Notification(f'{package_name} installed!', 'Installation successful.').show()

def main():
    """
    Main function to initialize and run the LazyCat application.
    """
    app = LazyCat()
    Gtk.main()

if __name__ == '__main__':
    main()
