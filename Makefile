#/usr/bin/sh
# Build Mishkal Package
default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all: 

# Publish to github
publish:
	git push origin master 

date=$(shell date +'%y.%m.%d-%H:%M')
doc:
	epydoc -v --config epydoc.conf
test2:
	python2 bin/mishkal-console.py --progress -c -f tests/samples/phrases.txt >tests/output/test2.csv
test3:
	python3 bin/mishkal-console.py --progress -c -f tests/samples/phrases.txt >tests/output/test3.csv
test2l:
	python2 bin/mishkal-console.py -c -l 2 -f tests/samples/phrases.txt >tests/output/test2.csv
test3l:
	python3 bin/mishkal-console.py -c -l 2 -f tests/samples/phrases.txt >tests/output/test3.csv

server:
	python3 interfaces/web/mishkal_bottle.py
gui:
	python3 interfaces/gui/mishkal-gui.py
console:
	python3 bin/mishkal-console.py
