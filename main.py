
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, Pango, GLib

# Create a new terminal widget
terminal = Vte.Terminal()

# Set the font size to 14
font_desc = Pango.FontDescription('monospace 14')
terminal.set_font(font_desc)

# Create a text box
text_box = Gtk.Entry()

# Create a button
button = Gtk.Button(label="Run Command")

# Create a vertical box to hold the terminal, text box, and button
vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
vbox.pack_start(terminal, True, True, 0)
vbox.pack_start(text_box, False, False, 0)
vbox.pack_start(button, False, False, 0)

# Create a GTK window
win = Gtk.Window()
win.connect('destroy', Gtk.main_quit)
win.add(vbox)
win.show_all()

# Function to handle the button click
def on_button_clicked(button):
    command = text_box.get_text()
    if command:
        # Feed the command to the terminal
        terminal.feed_child(command + '\n')  # Add a newline to execute the command

# Connect the button to the click handler
button.connect('clicked', on_button_clicked)

# Function to handle the terminal's child-exit signal
def on_child_exited(terminal, pid):
    print(f"Child process with PID {pid} has exited")
    # Optionally, you can close the window or restart the shell
    terminal.spawn_async(
        Vte.PtyFlags.DEFAULT,
        None,  # Working directory (None means use the home directory)
        ["/bin/bash"],  # Command to run
        [],  # Environment variables
        GLib.SpawnFlags.DO_NOT_REAP_CHILD,
        None,  # Child setup function
        None,  # User data for child setup function
        -1,  # Timeout
        None,  # Cancellable
        on_spawn_complete  # Callback function for spawn completion
    )

# Function to handle the spawn completion
def on_spawn_complete(terminal, success, pid, error):
    if not success:
        print(f"Failed to spawn shell: {error}")
        return
    print(f"Shell spawned with PID {pid}")

# Start a shell in the terminal
result = terminal.spawn_async(
    Vte.PtyFlags.DEFAULT,
    None,  # Working directory (None means use the home directory)
    ["/bin/bash"],  # Command to run
    [],  # Environment variables
    GLib.SpawnFlags.DO_NOT_REAP_CHILD,
    None,  # Child setup function
    None,  # User data for child setup function
    -1,  # Timeout
    None,  # Cancellable
    on_spawn_complete  # Callback function for spawn completion
)

if result is None:
    print("Failed to start the shell. Check the error message for details.")
else:
    pid, = result

# Run the GTK main loop
Gtk.main()
