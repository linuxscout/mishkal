#! /usr/bin/python
from distutils.core import setup
from glob import glob
import sys
sys.path.append("lib");
import py2exe
setup(name='Mishkal Softwares', version='0.2',
      description='Mishkal Softwares',
      author='Taha Zerrouki',
      author_email='taha.zerrouki@gmail.com',
      url='http://tashkeel.qutrub.org/',
      license='GPL',
	 windows = [
        {
            "script": "mishkal-gui.py",
            "icon_resources": [(1, "./ar/images/ix.ico")],
			
        }],
	console = [
		
        {
            "script": "mishkal-console.py",
            "icon_resources": [(1, "./ar/images/ixn.ico")],
			
        }		
,
        {
            "script": "mishkal-webserver.py",
            "icon_resources": [(1, "./ar/images/weblogo.ico")],
			
        }				
    ],

      classifiers=[
          'Development Status :: 5 - Beta',
          'Intended Audience :: End Users/Desktop',
          'Operating System :: OS independent',
          'Programming Language :: Python',
          ],
		  options = {
            "py2exe": {
            "compressed": 1,
            "optimize": 2,
            "bundle_files": 2,
            # "dll_excludes": [  "MSVCP90.dll", ],
			 "includes":["sip"],
                      }
					}, 
 
      data_files=[
	  #images
	  # ('images',[
	  # './images/logo.png','./images/sma.ico',]),
		#data
	  ('data',  [  './data/randomtext.txt',
					'./data/collocations.sqlite',
					# r'./lib/qalsadi/data/*.sqlite',
					'./lib/arramooz/data/arabicdictionary.sqlite',					
					'./lib/arramooz/data/stopwords.sqlite',
					'./lib/arramooz/data/wordfreq.sqlite',
			]
    	),
		#data
	  #('aranalex/data',  [  './aranalex/data/verbs.sqlite',   ]  ),

	  #docs
	  ('docs',
	   [
	   # r'./docs/*.*',
	   './docs/AUTHORS.txt',
		'./docs/THANKS.txt',
		'./docs/ChangeLog.txt',
		'./docs/COPYING.txt',
		'./docs/README.txt',
		'./docs/TODO.txt',
		'./docs/VERSION.txt',		
	   ]
       ),  
	   
	  ('ar',
	   [ #r'./ar/*.*',
	   './ar/style.css',
	   './ar/projects.html',
       './ar/about.html',
       './ar/help_body.html'
	   ]
       ),
	  ('ar/images',
	  [	  #r'./ar/images/*.*',
	   './ar/images/alef_wasla.png',
	'./ar/images/animation.png',
	'./ar/images/appicon.ico',
	'./ar/images/appicon.png',
	'./ar/images/copy.png',
	'./ar/images/cut.png',
	'./ar/images/damma.png',
	'./ar/images/dammatan.png',
	'./ar/images/exit.png',
	'./ar/images/fatha.png',
	'./ar/images/fathatan.png',
	'./ar/images/font.png',
	'./ar/images/gaf.png',
	'./ar/images/help.jpg',
	'./ar/images/icon.png',
	'./ar/images/kasra.png',
	'./ar/images/kasratan.png',
	'./ar/images/logo.png',
	'./ar/images/new.png',
	'./ar/images/open.png',
	'./ar/images/paste.png',
	'./ar/images/peh.png',
	'./ar/images/preview.png',
	'./ar/images/print.png',
	'./ar/images/qutrub.ico',
	'./ar/images/save.png',
	'./ar/images/shadda.png',
	'./ar/images/smallalef.PNG',
	'./ar/images/sukun.png',
	'./ar/images/tatweel.PNG',
	'./ar/images/text-speak.png',
	'./ar/images/Thumbs.db',
	'./ar/images/zoomin.png',
	'./ar/images/zoomout.png',
	'./ar/images/zwj.png',
	'./ar/images/zwnj.png',

	])
	,
	
	
		  #resources/
	  # ('resources',
	   # [,
	   # ]
       # ),  
	   
	  #resources/templates
	  ('resources/templates',
	   ['./resources/templates/500.html',
		'./resources/templates/contact.html',
		'./resources/templates/doc.html',
		'./resources/templates/download.html',
		'./resources/templates/link.html',
		'./resources/templates/log.html',
		'./resources/templates/main.html',
		'./resources/templates/projects.html',
		'./resources/templates/whoisqutrub.html',
	   ]
       ),  
	   
	  #resources/files
	  ('resources/files',
	   ['resources/files/adawat.js',
		'resources/files/adawat.png',
		'resources/files/adawatstyle.css',
		'resources/files/f.png',
		'resources/files/favicon.png',
		'resources/files/get_ffx.png',
		'resources/files/jquery-1.7.1.min.js',
		'resources/files/jquery.history.min.js',
		'resources/files/jquery.min.js',
		'resources/files/loading.gif',
		'resources/files/logo.png',
		'resources/files/logverb.txt',
		'resources/files/qamoos.css',
		'resources/files/qamoos.js',
		'resources/files/style.css',
	   ]
       ),  		   
	   
	  #resources/images
	  ('resources/files/images',
	   ['resources/files/images/ActiveMenuButton.png',
		'resources/files/images/ActiveMenuButtonAnchor.png',
		'resources/files/images/ArticleCenter.png',
		'resources/files/images/ArticleCorners.png',
		'resources/files/images/ArticleHorizontal.png',
		'resources/files/images/ArticleVertical.png',
		'resources/files/images/BackgroundGradient.png',
		'resources/files/images/BlockCenter.png',
		'resources/files/images/BlockCorners.png',
		'resources/files/images/BlockHeader.png',
		'resources/files/images/BlockHeaderAnchor.png',
		'resources/files/images/BlockHorizontal.png',
		'resources/files/images/BlockVertical.png',
		'resources/files/images/BorderCenter.png',
		'resources/files/images/BorderCorners.png',
		'resources/files/images/BorderHorizontal.png',
		'resources/files/images/BorderVertical.png',
		'resources/files/images/Button.png',
		'resources/files/images/ButtonAnchor.png',
		'resources/files/images/Footer.png',
		'resources/files/images/Header.png',
		'resources/files/images/MenuBar.png',
		'resources/files/images/MenuButton.png',
		'resources/files/images/MenuButtonAnchor.png',
	   ]
       ),  		   
	   
	# end datafiles
	  ] 
	 #end setup
 )