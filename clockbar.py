from gi.repository import GLib, Gtk

def clockbar_init(window):
    def update_time():
        from datetime import datetime
        now = datetime.now()
        time_str = now.strftime("lazycat - %H:%M:%S | %d %B %Y")
        window.set_title(time_str)
        return True  # Continue calling every timeout interval

    GLib.timeout_add(1000, update_time)
