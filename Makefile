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
# run
server:
	python3 interfaces/web/mishkal_bottle.py
gui:
	python3 interfaces/gui/mishkal-gui.py
console:
	python3 bin/mishkal-console.py

#build
md2rst:
	pandoc -s -r markdown -w rst README.md -o README.rst
md2html:
	pandoc -s -r markdown -w html README.md -o README.html
	
wheel:
	sudo python setup.py bdist_wheel
wheel3:
	sudo python3 setup.py bdist_wheel
sdist:
	sudo python3 setup.py sdist
sdist2:
	sudo python setup.py sdist
upload:
	echo "use twine upload dist/mishkal-0.1.tar.gz"
install:
	sudo python setup.py install
install3:
	sudo python3 setup.py install


# tests
test2l:limit=-l 2
test2 test2l:
	# test on python 2
	python2 bin/mishkal-console.py --progress ${limit} -c -f tests/samples/phrases.txt >tests/output/test2.csv
test3l:limit=-l 2
test3 test3l:
	python3 bin/mishkal-console.py --progress ${limit} -c -f tests/samples/phrases.txt >tests/output/test3.csv
profile3:
	python3 -m cProfile -o tests/output/phrases.profile  bin/mishkal-console.py --progress -c -f tests/samples/phrases.txt >tests/output/test3.csv


# eval
#~FILE="adab.txt"
#FILE="rndlines.txt"
jazeera:FILE="aljazeera.txt"
jazeera:limit=5
#~ jazeera:profiler=-m cProfile  -o output/mishkal.profile
jazeera:profiler=-m cProfile 
jazeera:
	cd tests;python3  ${profiler} ../bin/mishkal-console.py --cache --progress -c -l ${limit} -f samples/vocalized/${FILE} >output/compare/rndlines.11.txt
	echo "make archive" 
	cd tests;cp output/compare/rndlines.11.txt  output/compare/L${date}.txt
	echo "save stats"
	cd tests;date >> output/compare/file.stats  
#~ 	cd tests;grep "function calls" -2 -h output/compare/rndlines.11.txt | sed 's/^.*function .* in //g;s/:\*.*$//g' | sed 'N;s/\n//g' >> output/compare/file.stats
	cd tests;grep "function calls" -h output/compare/rndlines.11.txt > /tmp/lines.tmp
	sed "s/^.*function .* in //g;s/:\*.*$$//g" -i /tmp/lines.tmp
	sed "N;s/\n//g" -i /tmp/lines.tmp
	cd tests;cat /tmp/lines.tmp>> output/compare/file.stats
	cd tests;tail -n 3 output/compare/file.stats
