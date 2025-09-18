#!/usr/bin/make -f
# ----------------------------------------
# Mishkal Makefile - Arabic Diacritizer
# https://github.com/linuxscout/mishkal
# ----------------------------------------

.PHONY: default all clean backup run console flask gui server \
		build sdist wheel upload install \
		test2 test3 test2l test3l profile \
		jazeera compare \
		md2rst md2html doc exe-gui help

PYTHON=python3
DATE=$(shell date +'%y.%m.%d-%H:%M')

# ----------------------------------------
# Default
# ----------------------------------------
default: all

all:
	@echo "Build all components - placeholder"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build dist *.egg-info
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +

backup:
	@echo "Backup logic placeholder"

# ----------------------------------------
# Run interfaces
# ----------------------------------------
server:
	$(PYTHON) interfaces/web/mishkal_bottle.py

flask:
	$(PYTHON) interfaces/web/mishkal_flask.py

gui:
	$(PYTHON) interfaces/gui/mishkal-gui.py

console:
	$(PYTHON) bin/mishkal-console.py

# ----------------------------------------
# Build and Packaging
# ----------------------------------------
md2rst:
	pandoc -s -r markdown -w rst README.md -o README.rst

md2html:
	pandoc -s -r markdown -w html README.md -o README.html

sdist:
	$(PYTHON) setup.py sdist

wheel:
	$(PYTHON) setup.py bdist_wheel

upload:
	@echo "Uploading with twine..."
	echo "use twine upload dist/mishkal-0.1.tar.gz"

install:
	$(PYTHON) setup.py install

# ----------------------------------------
# Testing
# ----------------------------------------
test2l: limit=-l 2
test2 test2l:
	python2 bin/mishkal-console.py --progress $(limit) --eval -f tests/samples/phrases.txt > tests/output/test2.csv

test3l: limit=-l 2
test3 test3l:
	$(PYTHON) bin/mishkal-console.py --progress $(limit) --eval -f tests/samples/phrases.txt > tests/output/test3.csv

profile:
	$(PYTHON) -m cProfile -o tests/output/phrases.profile bin/mishkal-console.py --progress --eval -f tests/samples/phrases.txt > tests/output/test3.csv

# ----------------------------------------
# Evaluation and comparison
# ----------------------------------------
jazeera: FILE="aljazeera.txt" limit=2000 profiler=-m cProfile
jazeera:
	cd tests; $(PYTHON) $(profiler) ../bin/mishkal-console.py --progress --eval -l $(limit) -f samples/vocalized/$(FILE) > output/compare/rndlines.11.txt
	cd tests; cp output/compare/rndlines.11.txt output/compare/L$(DATE).txt
	cd tests; date >> output/compare/file.stats
	cd tests; head -n 3 output/compare/rndlines.11.txt > /tmp/lines.tmp
	cd tests; grep "function calls" --no-filename --before-context=2 output/compare/rndlines.11.txt >> /tmp/lines.tmp
	cd tests; cat /tmp/lines.tmp >> output/compare/file.stats
	cd tests; tail -n 6 output/compare/file.stats

compare: FILE=phrases.txt limit=10
compare:
	cd tests;$(PYTHON) ../bin/mishkal-console.py --progress --eval -l $(limit) -f samples/$(FILE) --compareto samples/$(FILE) > output/compare/compare.txt

nemlar2: FILE=nemlar.txt limit=1000
nemlar2:
	cd tests;$(PYTHON) ../bin/mishkal-console.py --progress --eval -l $(limit) -f samples/$(FILE) --compareto samples/$(FILE) > output/compare/compare.txt

# ----------------------------------------
# Executable GUI using PyInstaller
# ----------------------------------------
exe-gui:
	pyinstaller mishkal-gui.spec

# ----------------------------------------
# Docs (if epydoc used)
# ----------------------------------------
doc:
	epydoc -v --config epydoc.conf

# ----------------------------------------
# Help message
# ----------------------------------------
help:
	@echo "Mishkal Makefile Targets:"
	@echo "  run / server / flask / gui / console - Run interfaces"
	@echo "  build / sdist / wheel / upload / install - Packaging"
	@echo "  test2 / test3 / profile / jazeera / compare - Testing and Evaluation"
	@echo "  clean / backup / help"

nemlar:
	cd tests && $(PYTHON) nemlar_eval.py samples/Nemlar --csv output/results.csv  --limit 50

nemlar2: FILE=nemlar.txt
nemlar2:limit=1000
nemlar2:
	cd tests && $(PYTHON) ../bin/mishkal-console.py --progress --eval -l $(limit) -f samples/$(FILE) > output/compare/compare.txt
