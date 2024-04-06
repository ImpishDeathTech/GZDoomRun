install:
	python3 -m pip install pysimplegui
	python3 -m pip install ./
	sudo mkdir /usr/share/gzdoomrun	
	sudo cp LICENSE /usr/share/gzdoomrun
	sudo cp VERSION /usr/share/gzdoomrun
	sudo cp -r build /usr/share/gzdoomrun
	chmod +x ./uninstall
	sudo cp ./uninstall /usr/share/gzdoomrun
	sudo cp *.png /usr/share/gzdoomrun 
	sudo cp *.jpg /usr/share/gzdoomrun 
	sudo cp gzdoomrun.desktop /usr/share/applications
	chmod +x ./gzdr.sh
	sudo cp ./gzdr.sh /usr/bin
	cp modcache.json $(HOME)/.config/gzdoom 
	cp -r custom $(HOME)/.config/gzdoom

uninstall:
	python3 -m pip uninstall gzdoomrun 
	sudo rm -r /usr/share/gzdoomrun
	sudo rm -r $(HOM)/.config/gzdoom/custom 
	sudo rm /usr/share/applications/gzdoomrun.desktop
	
