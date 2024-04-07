PY3      = python3 -m 
INSTALL  = pip install
UNINSTALL= pip uninstall
GZDR_DIR = /usr/share/gzdoomrun 
APPS     = /usr/share/applications
BIN      = /usr/bin/gzdrun

.venv:
	$(PY3) venv $(HOME)/.venv
	$(PY3) venv $(HOME)/.venv/bin/activate

install:
	sudo mkdir $(GZDR_DIR)
	sudo cp LICENSE $(GZDR_DIR)
	sudo cp VERSION $(GZDR_DIR)
	sudo cp -r build $(GZDR_DIR)
	sudo cp *.png $(GZDR_DIR) 
	sudo cp *.jpg $(GZDR_DIR) 
	sudo cp gzdoomrun.desktop $(APPS)
	
	chmod +x gzdrun.sh 
	sudo cp gzdrun.sh /usr/bin/gzdrun
	sudo cp activate.sh /usr/bin/activate
	cp modcache.json $(HOME)/.config/gzdoom 
	cp -r custom $(HOME)/.config/gzdoom

	$(PY3) $(INSTALL) pysimplegui
	$(PY3) $(INSTALL) ./

uninstall:
	$(PY3) $(UNINSTALL) GZDoomRun
	sudo rm -r $(GZDR_DIR)
	sudo rm $(BIN)
	sudo rm -r $(HOME)/.config/gzdoom/custom 
	sudo rm /usr/share/applications/gzdoomrun.desktop
	
