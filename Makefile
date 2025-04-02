# Target to run the main Python script
run:
	python3 main.py

# Target to install the LazyCat application
install:
	# Make the main script executable
	chmod +x main.py
	
	# Remove any existing LazyCat installation
	sudo rm -rf /opt/lazycat
	sudo rm /usr/bin/lazycat
	
	# Create the installation directory
	sudo mkdir -p /opt/lazycat
	
	# Copy the project files to the installation directory
	sudo cp -rf . /opt/lazycat
	
	# Copy the desktop file to the system and user application directories
	sudo cp -rf ./xdg/lazycat.desktop /usr/share/applications
	cp -rf ./xdg/lazycat.desktop ~/.local/share/applications
	
	# Copy the icon to the system icon directories
	sudo cp -rf ./icon/lazycat.png /usr/share/icons/hicolor/256x256/apps/
	sudo cp -rf ./icon/lazycat.png /usr/share/icons/
	
	# Create a symbolic link to the main script in the system's bin directory
	sudo ln -s /opt/lazycat/main.py /usr/bin/lazycat
	
	# Confirmation message
	@echo 'LazyCat installed ...'
