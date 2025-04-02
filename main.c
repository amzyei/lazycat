#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <vte/vte.h>
#include <gtk/gtk.h>
#include <glib.h>

#define NOTIFY_SEND "notify-send "

GtkWidget *win, *terminal, *first_box, *second_box, *third_box, *install_button, *exec_label, *exec_entry;

static void child_ready(VteTerminal *terminal, GPid pid, GError *error, gpointer user_data) {
    if (!terminal) return;
    if (pid == -1) gtk_main_quit();
}

static void install_package(void) {
    const gchar *package_name = gtk_entry_get_text(GTK_ENTRY(exec_entry));
    if (package_name == NULL || strlen(package_name) == 0) {
        system("notify-send \"Error\" \"Please enter a package name\"");
        return;
    }

    const char *install_command = "pkexec apt install -y ";
    char *full_command = g_strdup_printf("%s%s", install_command, package_name);

    int result = system(full_command);
    g_free(full_command);

    if (result == 0) {
        char *notify_message = g_strdup_printf("%s \"%s installed!\"", NOTIFY_SEND, package_name);
        system(notify_message);
        g_free(notify_message);
    } else {
        system("notify-send \"Error\" \"Package not found\"");
    }
}

int main(int argc, char *argv[]) {
    char *home_dir = getenv("HOME");
    if (home_dir == NULL) {
        fprintf(stderr, "Error: HOME environment variable not set\n");
        return 1;
    }

    char *logo_path = "/.lazyCat/icon/lazyCat.png";
    int logo_path_len = strlen(logo_path);
    int full_path_len = strlen(home_dir) + logo_path_len + 1;

    char *icon_path = (char *)malloc(full_path_len * sizeof(char));
    if (icon_path == NULL) {
        fprintf(stderr, "Error: Failed to allocate memory for icon path\n");
        return 1;
    }

    snprintf(icon_path, full_path_len, "%s%s", home_dir, logo_path);

    gtk_init(&argc, &argv);

    win = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(win), "lazyCat");
    gtk_window_set_icon_from_file(GTK_WINDOW(win), icon_path, NULL);

    terminal = vte_terminal_new();
    vte_terminal_set_font_scale(VTE_TERMINAL(terminal), 1.3);

    first_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 0);
    second_box = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
    third_box = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);

    install_button = gtk_button_new_with_label("Install Package");
    exec_label = gtk_label_new("Enter package name: ");
    exec_entry = gtk_entry_new();

    gchar **envp = g_get_environ();
    gchar **command = (gchar *[]){g_strdup(g_environ_getenv(envp, "SHELL")), NULL };
    g_strfreev(envp);

    vte_terminal_spawn_async(VTE_TERMINAL(terminal),
                             VTE_PTY_DEFAULT,
                             home_dir,         /* working directory */
                             command,          /* command */
                             NULL,             /* environment */
                             2,                /* spawn flags */
                             NULL, NULL,       /* child setup */
                             NULL,             /* child pid */
                             -1,               /* timeout */
                             NULL,             /* cancellable */
                             child_ready,      /* callback */
                             NULL);            /* user_data */

    g_signal_connect(win, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    g_signal_connect(terminal, "child-exited", G_CALLBACK(gtk_main_quit), NULL);
    g_signal_connect(G_OBJECT(install_button), "clicked", G_CALLBACK(install_package), NULL);

    gtk_box_pack_start(GTK_BOX(first_box), terminal, TRUE, TRUE, 0);
    gtk_box_pack_end(GTK_BOX(first_box), second_box, FALSE, FALSE, 0);
    gtk_box_pack_end(GTK_BOX(first_box), third_box, FALSE, FALSE, 0);

    gtk_box_pack_end(GTK_BOX(second_box), install_button, TRUE, TRUE, 4);
    gtk_box_pack_start(GTK_BOX(third_box), exec_label, FALSE, FALSE, 4);
    gtk_box_pack_start(GTK_BOX(third_box), exec_entry, FALSE, FALSE, 4);

    gtk_container_add(GTK_CONTAINER(win), first_box);

    free(icon_path);
    g_free(command[0]);

    gtk_widget_show_all(win);

    gtk_main();

    return 0;
}
