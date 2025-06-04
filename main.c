/*
 * Main entry point for LazyCat terminal emulator in C.
 * This program initializes GTK and integrates the clockbar functionality and a lightweight VTE terminal.
 *
 * This program is free software: you can change and share it under
 * the rules of the GNU General Public License from the Free Software
 * Foundation, version 3 or later.
 *
 * This program is shared in the hope it will be useful, but WITHOUT
 * ANY WARRANTY; no guarantee of being good or fit for any purpose.
 * See the GNU General Public License for more details.
 * You should have a copy of the GNU General Public License with this program.
 * If not, see <http://www.gnu.org/licenses/>.
 * [AMZYEI]
 */

#include <gtk/gtk.h>
#include <vte-2.91/vte/vte.h>
#include <time.h>

#include "include/clockbar.h"

static gboolean update_time(gpointer user_data) {
    GtkWindow *window = GTK_WINDOW(user_data);
    time_t rawtime;
    struct tm *timeinfo;
    char buffer[80];

    time(&rawtime);
    timeinfo = localtime(&rawtime);

    strftime(buffer, sizeof(buffer), "lazycat - %H:%M:%S | %d %B %Y", timeinfo);
    gtk_window_set_title(window, buffer);

    return TRUE; // Keep calling every 1 second
}

int main(int argc, char *argv[]) {
    GtkWidget *window;
    GtkWidget *terminal;
    VteTerminal *vte_terminal;
    GError *error = NULL;

    gtk_init(&argc, &argv);

    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_default_size(GTK_WINDOW(window), 800, 600);
    gtk_window_set_title(GTK_WINDOW(window), "lazycat");

    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    // Create VTE terminal widget
    vte_terminal = VTE_TERMINAL(vte_terminal_new());
    terminal = GTK_WIDGET(vte_terminal);

    // Start a shell in the terminal
    GPid child_pid;
    gboolean success = vte_terminal_spawn_sync(vte_terminal,
                           VTE_PTY_DEFAULT,
                           NULL,               // working directory
                           (char *[]){getenv("SHELL"), NULL}, // argv
                           NULL,               // environment
                           0,                  // spawn flags
                           NULL,               // child setup
                           NULL,               // child setup data
                           &child_pid,         // child pid
                           NULL,               // cancellable
                           &error);

    if (error != NULL) {
        g_warning("Failed to start shell: %s", error->message);
        g_clear_error(&error);
    }

    gtk_container_add(GTK_CONTAINER(window), terminal);

    // Start clockbar to update window title
    clockbar_init(window);

    gtk_widget_show_all(window);

    gtk_main();

    return 0;
}
