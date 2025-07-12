# Makefile for Python version of LazyCat

.PHONY: run install

run:
	python3 main.py

install:
	@echo "Installing LazyCat Python version system-wide..."
	install -d /usr/local/bin
	install -m 755 main.py /usr/local/bin/lazycat

	# Install icon
	sudo install -Dm644 icon/lazycat.png /usr/share/icons/hicolor/256x256/apps/lazycat.png
	sudo install -Dm644 icon/lazycat.png /usr/share/icons/lazycat.png

	# Install desktop entry
	sudo install -Dm644 xdg/lazycat.desktop /usr/share/applications/lazycat.desktop
	install -Dm644 xdg/lazycat.desktop ~/.local/share/applications/lazycat.desktop

	@echo "Installation complete. You can run the app using 'lazycat' command."
