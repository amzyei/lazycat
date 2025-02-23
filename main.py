#!/usr/bin/env python
import gi 
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')

from gi.repository import Gtk, Vte
from gi.repository import GLib
from os import system, environ 

terminal     = Vte.Terminal()
terminal.spawn_sync(
    Vte.PtyFlags.DEFAULT,
    environ['HOME'],
    ['%s' % 'zsh' if system('ls /bin/zsh') == 0 else 'sh'],
    [],
    GLib.SpawnFlags.DO_NOT_REAP_CHILD,
    None,
    None,
    )

win = Gtk.Window()
win.connect('delete-event', Gtk.main_quit)
win.add(terminal)
win.show_all()

Gtk.main()
