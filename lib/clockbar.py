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
import time
import random
from gi.repository import Gtk, GLib

class Clock:
    def __init__(self, window):
        self.window = window
        self.update_time()

    def update_time(self):
        current_time = time.strftime('%H:%M:%S | %d %B %Y ')
        self.window.set_title(f'lazycat - {current_time}')
        self.timeout_id = GLib.timeout_add(1000, self.update_time)
