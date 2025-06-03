/*
 * Clockbar implementation in C using GTK
 * This program updates the window title every second with the current time.
 * 
 * This program is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with
 * this program. If not, see <http://www.gnu.org/licenses/>.
 * [AMZYEI]
 */

#include <gtk/gtk.h>
#include <time.h>

static gboolean clockbar_update_time(gpointer user_data) {
    GtkWindow *window = GTK_WINDOW(user_data);
    time_t rawtime;
    struct tm *timeinfo;
    char buffer[80];

    time(&rawtime);
    timeinfo = localtime(&rawtime);

    strftime(buffer, sizeof(buffer), "lazycat - %H:%M:%S | %d %B %Y", timeinfo);
    gtk_window_set_title(window, buffer);

    return TRUE; // Continue calling every timeout interval
}

void clockbar_init(GtkWidget *window) {
    // Call clockbar_update_time every 1000 milliseconds (1 second)
    g_timeout_add(1000, clockbar_update_time, window);
}
