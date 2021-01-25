PY = python3
SRC = src/
ARCHIVE = metro_project

run:
	# python3 src/metro.py
	$(PY) $(SRC)metro_v2.py

archive:
	rm -Rf *.tar
	mkdir -p $(ARCHIVE)
	cp -R src/ $(ARCHIVE)
	cp metro.txt $(ARCHIVE)
	cp Makefile $(ARCHIVE)
	cp README.md $(ARCHIVE)
	tar -zcvf $(ARCHIVE).tar $(ARCHIVE)
	rm -Rf $(ARCHIVE)
