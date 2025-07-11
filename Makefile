# Short description of this Python module.
# Longer description of this module.
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
# [AMZYEI]

# Target to run the main C program
run:
	gcc main.c include/clockbar.c -o lazycat `pkg-config --cflags --libs gtk+-3.0 vte-2.91` && ./lazycat

# Target to install dependencies
deps:
	sudo apt-get update && sudo apt-get install -y build-essential pkg-config libgtk-3-dev libvte-2.91-dev

# Target to install the LazyCat application
install:

	# Remove any existing LazyCat installation
	sudo rm -rf /opt/lazycat
	sudo rm -rf /usr/bin/lazycat
	
	# Copy the desktop file to the system and user application directories
	sudo cp -rf ./xdg/lazycat.desktop /usr/share/applications
	cp -rf ./xdg/lazycat.desktop ~/.local/share/applications
	
	# Copy the icon to the system icon directories
	sudo cp -rf ./icon/lazycat.png /usr/share/icons/hicolor/256x256/apps/
	sudo cp -rf ./icon/lazycat.png /usr/share/icons/
	
	# Create a bin file to the /usr/bin
	gcc main.c include/clockbar.c -o lazycat `pkg-config --cflags --libs gtk+-3.0 vte-2.91`
	strip lazycat && sudo cp -rf lazycat /usr/bin
	# Confirmation message
	@echo 'LazyCat installed ...'
