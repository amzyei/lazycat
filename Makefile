run:
	python3 main.py

install: 
	chmod +x main.py
	sudo rm -rf /opt/lazycat && sudo rm /usr/bin/lazycat && sudo mkdir -p /opt/lazycat && sudo cp -rf . /opt/lazycat
	sudo cp -rf ./xdg/lazycat.desktop /usr/share/applications
	cp -rf ./xdg/lazycat.desktop ~/.local/share/applications
	sudo cp -rf ./icon/lazycat.png /usr/share/icons/hicolor/256x256/apps/
	sudo cp -rf ./icon/lazycat.png /usr/share/icons/hicolor/256x256/apps/
	sudo cp -rf ./icon/lazycat.png /usr/share/icons/
	sudo ln /opt/lazycat/main.py /usr/bin/lazycat
	@echo 'LazyCat installed ...'

