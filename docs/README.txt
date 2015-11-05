Mishkal : Arabic text vocalization system
مشكال لتشكيل النصوص العربية
This program is licensed under the GPL License
Developpers:
	Taha Zerrouki: http://tahadz.com
	taha dot zerrouki at gmail dot com


Site:
==========
http://tahadz.com
Download
==========
http://mishkal.sourceforge.net
Source
=============
http://svn.arabeyes.org
http://github.com/linuxscout/mishkal


Usage
=====
* Windows :
-----------
Run MishkalGui

* GUI: Linux
---------------
 - mishkal-gui
*Web server (linux, windows)
-----------
  mishkal-webserver
  serving on 0.0.0.0:8080 view at http://127.0.0.1:8080
  open in your browser the URL: http://127.0.0.1:8080

* Console (linux/windows)
-----------------
 Usage: mishkal-console -f filename [OPTIONS]
        mishkal-console 'السلام عليكم' [OPTIONS]

	[-f | --file= filename]input file to mishkal-console
	[-i | --ignore]   ignore the last Mark on output words.
	[-r | --reduced]  Reduced Tashkeel.
	[-s | --strip]    Strip tashkeel (remove harakat).
	[-h | --help]     outputs this usage message
	[-v | --version]  program version
	[-l | --limit]    vocalize only a limited number of line
	[-x | --syntax]   disable syntaxic analysis
	[-m | --semantic] disable semantic analysis
	[-c | --compare]  compare the vocalized text with the program output
	[-t | --stat]     disable statistic tashkeel

This program is licensed under the GPL License


Files
=====
file/directory	category	description 
[program]
	mishkal-console.py	program	Mishkal script used on shell command
	mishkal-gui.py	program	launch mishkal GUI interface with QT
	mishkal-webserver.py	web	lauch mishkal web server

[docs]
	docs/	docs	documentation
[setup]
	exe_setup.py	setup	prepare setup for windows using py2exe
	setup.py	setup	setup for library and linux package
[mishkal]
	aranasyn/	src	Arabic syntaxic analyzer
	asmai/	src	Arabic syntaxic analyzer
	core/	src	basic tools
	gui/	src	GUI source
	tashkeel/	src	Tashkeel module source
[lib]
	lib/	lib	Libraries
[data]
	data/	data	databases files
[resouces]
	ar/	resources	reources for gui arabic
[log]
	tmp/	log	tomporary fdirectory for web service
[tools]
	cleanpyc	setup	a shell script to remove .pyc files
[test]
	output/	test	test output
	samples/	test	sample files
	tools/	test	script to use mishkal
[web]
	files/	web	files used for web service
	templates/	web	Templates used for web service
	adawaty.py	web	a script for web service
	cgirunner.py	web	a script for web service using cgi
	crossdomain.xml	web	Configuration file to allow cross domain json API
	index.html	web	an index file to avoid directory access
	mishkal.cgi	web	A cgi Script used on web service
	mishkal-webserver.py	web	lauch mishkal web server
[apps]
	mintiq	TTS	a shell script to join mishkla with espeak Text to speech

JSON connection API:
-----------------
view docs/html/index.html (in arabic)
