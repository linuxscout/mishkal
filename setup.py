#! /usr/bin/python
from distutils.core import setup
from glob import glob
import py2exe

# to install type:
# python setup.py install --root=/

setup (name='SalamScout Softwares', version='0.5',
      description='Mishkal Softwares',
      author='Taha Zerrouki',
      author_email='taha.zerrouki@gmail.com',
      url='http://tashkeel.qutrub.org/',
      license='GPL',
	 console = [
        {
            "script": "scoutgameconsole.py",
            "icon_resources": [(1, "favicon.ico")]
        }
    ],
	 windows = [
        {
            "script": "main_gui.py",
            "icon_resources": [(1, "favicon.ico")]
        }
    ],

      #scripts=['Qutrub'],
      classifiers=[
          'Development Status :: 5 - Beta',
          'Intended Audience :: End Users/Desktop',
          'Operating System :: OS independent',
          'Programming Language :: Python',
          ],
      data_files=[
	  #('images',['f:\gui/qutrub/libqutrub/images/save.png']),
	  ('images',[
	  './images/logo.png','./images/sma.ico',]),

	  ('data',
	   [ 
	   ]
       ),
	  ('ar',
	   ['./ar/style.css',
	   './ar/projects.html',
       './ar/about.html',
       './ar/help_body.html']
       ),
	  ('ar/images',
	  [	  './ar/images/print.png',
	  './ar/images/save.png',
	  './ar/images/preview.png',
	  './ar/images/copy.png',
	  './ar/images/cut.png',
	  './ar/images/font.png',
	  './ar/images/help.jpg',
	  './ar/images/new.png',
	  './ar/images/exit.png',
	  './ar/images/zoomin.png',
	  './ar/images/zoomout.png',
	  './ar/images/logo.png' ])
	  ]);

