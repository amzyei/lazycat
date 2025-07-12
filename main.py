import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib
import os
import sys
from clockbar import clockbar_init

def spawn_shell(vte_terminal):
    shell = os.environ.get("SHELL", "/bin/bash")
    pty_flags = Vte.PtyFlags.DEFAULT
    def on_spawn_complete(terminal, task, user_data):
        try:
            task.wait()
        except GLib.Error as e:
            print(f"Failed to spawn shell: {e.message}", file=sys.stderr)
            Gtk.main_quit()

    vte_terminal.spawn_async(
        pty_flags,
        os.environ.get("HOME", "/"),
        [shell],
        [],
        GLib.SpawnFlags.DO_NOT_REAP_CHILD,
        None,
        None,
        -1,
        None,
        on_spawn_complete,
        None,
    )

def main():
    window = Gtk.Window(title="lazycat")
    window.set_default_size(800, 600)

    vte_terminal = Vte.Terminal()
    window.add(vte_terminal)

    window.connect("destroy", Gtk.main_quit)

    vte_terminal.connect("child-exited", lambda term: Gtk.main_quit())

    spawn_shell(vte_terminal)

    clockbar_init(window)

    window.show_all()

    Gtk.main()

if __name__ == "__main__":
    main()
