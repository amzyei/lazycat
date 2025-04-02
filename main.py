#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib, Pango

class LazyCatTerminal(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='LazyCat Terminal ')
        self.set_default_size(600, 400)

        # Create the VTE terminal
        self.terminal = Vte.Terminal()
        self.terminal.set_font(Pango.FontDescription('Monospace 16')) # Set the font size to 16

        # Create a Pty and associate it with the terminal
        pty = Vte.Pty.new_sync(Vte.PtyFlags.DEFAULT)
        self.terminal.set_pty(pty)

        # Spawn a shell in the terminal
        pty.spawn_async(
            None,
            ['/usr/bin/zsh' or '/bin/bash'],  # if ZSH not installed use the bash :)

            None,
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1,
            None,
            None
        )

        # Add the terminal to a scrolled window
        scroller = Gtk.ScrolledWindow()
        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        scroller.add(self.terminal)

        # Add the scrolled window to a box and then to the window
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(scroller, False, True, 2)
        self.add(box)


if __name__ == '__main__':
    win = LazyCatTerminal()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()
