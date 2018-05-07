#! /usr/bin/python
from setuptools import setup
import sys
sys.path.append("support");
sys.path.append("support/yaraspell");
sys.path.append("interfaces/web/lib");
sys.path.append("interfaces/web/lib/paste");
sys.path.append("interfaces/web/lib/simlejson");
sys.path.append("interfaces/web/lib/okasha2");
sys.path.append("interfaces/web");
sys.path.append("interfaces/gui");
sys.path.append("mishkal");
import py2exe
MyDataFiles = [

('data', ['./data/randomtext.txt']),

('docs', [
	'./docs/AUTHORS.txt',
	'./docs/ChangeLog.txt',
	'./docs/COPYING.txt',
	'./docs/HowTo.odt',
	'./docs/Ideas.odt',
	'./docs/ideas.txt',
	'./docs/README.txt',
	'./docs/THANKS.txt',
	'./docs/TODO.txt',
	'./docs/VERSION.txt',
]),

('docs/html/images',
	['./docs/html/images/adawatstyle.css',
	'./docs/html/images/gotashkeel.png',
	'./docs/html/images/mishkal.png',
	'./docs/html/images/mishkal_alpha_smpl.png',
	'./docs/html/images/mixkal.jpg',
	]
),


# ('interfaces/',[]),
# ('interfaces/gui/',[]),
# ('interfaces/gui/ar',
('ar',
	[
	'./interfaces/gui/ar/about.html',
	'./interfaces/gui/ar/help_body.html',
	# './interfaces/gui/ar/images',
	'./interfaces/gui/ar/projects.html',
	'./interfaces/gui/ar/style.css',
	]
),

# ('interfaces/gui/ar/images',
('ar/images',
	[
	'./interfaces/gui/ar/images/alef_wasla.png',
	'./interfaces/gui/ar/images/animation.png',
	'./interfaces/gui/ar/images/appicon.ico',
	'./interfaces/gui/ar/images/appicon.png',
	'./interfaces/gui/ar/images/copy.png',
	'./interfaces/gui/ar/images/cut.png',
	'./interfaces/gui/ar/images/damma.png',
	'./interfaces/gui/ar/images/dammatan.png',
	'./interfaces/gui/ar/images/exit.png',
	'./interfaces/gui/ar/images/fatha.png',
	'./interfaces/gui/ar/images/fathatan.png',
	'./interfaces/gui/ar/images/font.png',
	'./interfaces/gui/ar/images/gaf.png',
	'./interfaces/gui/ar/images/help.jpg',
	'./interfaces/gui/ar/images/icon.png',
	'./interfaces/gui/ar/images/ix.ico',
	'./interfaces/gui/ar/images/ixn.ico',
	'./interfaces/gui/ar/images/kasra.png',
	'./interfaces/gui/ar/images/kasratan.png',
	'./interfaces/gui/ar/images/logo.png',
	'./interfaces/gui/ar/images/new.png',
	'./interfaces/gui/ar/images/open.png',
	'./interfaces/gui/ar/images/paste.png',
	'./interfaces/gui/ar/images/peh.png',
	'./interfaces/gui/ar/images/preview.png',
	'./interfaces/gui/ar/images/print.png',
	'./interfaces/gui/ar/images/qutrub.ico',
	'./interfaces/gui/ar/images/save.png',
	'./interfaces/gui/ar/images/shadda.png',
	'./interfaces/gui/ar/images/smallalef.png',
	'./interfaces/gui/ar/images/sukun.png',
	# './interfaces/gui/ar/images/svg',
	'./interfaces/gui/ar/images/tatweel.png',
	'./interfaces/gui/ar/images/text-speak.png',
	'./interfaces/gui/ar/images/weblogo.ico',
	'./interfaces/gui/ar/images/zoomin.png',
	'./interfaces/gui/ar/images/zoomout.png',
	'./interfaces/gui/ar/images/zwj.png',
	'./interfaces/gui/ar/images/zwnj.png',

	],
),
# ('interfaces/gui/gui/',[]),
# ('interfaces/gui/gui/ar',
('gui/ar',
	[
	'./interfaces/gui/gui/ar/about.html',
	'./interfaces/gui/gui/ar/help_body.html',
	# './interfaces/gui/gui/ar/images',
	'./interfaces/gui/gui/ar/projects.html',
	'./interfaces/gui/gui/ar/style.css',
	]
),
# ('interfaces/gui/gui/ar/images',
('gui/ar/images',
	['./interfaces/gui/gui/ar/images/alef_wasla.png',
	'./interfaces/gui/gui/ar/images/animation.png',
	'./interfaces/gui/gui/ar/images/appicon.ico',
	'./interfaces/gui/gui/ar/images/appicon.png',
	'./interfaces/gui/gui/ar/images/copy.png',
	'./interfaces/gui/gui/ar/images/cut.png',
	'./interfaces/gui/gui/ar/images/damma.png',
	'./interfaces/gui/gui/ar/images/dammatan.png',
	'./interfaces/gui/gui/ar/images/exit.png',
	'./interfaces/gui/gui/ar/images/fatha.png',
	'./interfaces/gui/gui/ar/images/fathatan.png',
	'./interfaces/gui/gui/ar/images/font.png',
	'./interfaces/gui/gui/ar/images/gaf.png',
	'./interfaces/gui/gui/ar/images/help.jpg',
	'./interfaces/gui/gui/ar/images/icon.png',
	'./interfaces/gui/gui/ar/images/ix.ico',
	'./interfaces/gui/gui/ar/images/ixn.ico',
	'./interfaces/gui/gui/ar/images/kasra.png',
	'./interfaces/gui/gui/ar/images/kasratan.png',
	'./interfaces/gui/gui/ar/images/logo.png',
	'./interfaces/gui/gui/ar/images/new.png',
	'./interfaces/gui/gui/ar/images/open.png',
	'./interfaces/gui/gui/ar/images/paste.png',
	'./interfaces/gui/gui/ar/images/peh.png',
	'./interfaces/gui/gui/ar/images/preview.png',
	'./interfaces/gui/gui/ar/images/print.png',
	'./interfaces/gui/gui/ar/images/qutrub.ico',
	'./interfaces/gui/gui/ar/images/save.png',
	'./interfaces/gui/gui/ar/images/shadda.png',
	'./interfaces/gui/gui/ar/images/smallalef.png',
	'./interfaces/gui/gui/ar/images/sukun.png',
	# './interfaces/gui/gui/ar/images/svg',
	'./interfaces/gui/gui/ar/images/tatweel.png',
	'./interfaces/gui/gui/ar/images/text-speak.png',
	# './interfaces/gui/gui/ar/images/txt',
	'./interfaces/gui/gui/ar/images/weblogo.ico',
	'./interfaces/gui/gui/ar/images/zoomin.png',
	'./interfaces/gui/gui/ar/images/zoomout.png',
	'./interfaces/gui/gui/ar/images/zwj.png',
	'./interfaces/gui/gui/ar/images/zwnj.png',
	]
),
	


# ('',[]),
# ('resources/',[]),
('tmp',[]),

('resources/errorPages',
	[
	'./interfaces/web/resources/errorPages/400.shtml',
	'./interfaces/web/resources/errorPages/404.shtml',
	'./interfaces/web/resources/errorPages/500.shtml',
	# './interfaces/web/resources/errorPages/images',
	'./interfaces/web/resources/errorPages/Index.html',
	'./interfaces/web/resources/errorPages/logo.png',
	'./interfaces/web/resources/errorPages/images/logo.png',
	],
),
('resources/errorPages/images',
	['./interfaces/web/resources/errorPages/images/logo.png',
	],
),


('resources/files',
	[
	'./interfaces/web/resources/files/adawat.js',
	'./interfaces/web/resources/files/adawatstyle.css',
	'./interfaces/web/resources/files/cytoscape.min.js',
	'./interfaces/web/resources/files/favicon1.png',
	'./interfaces/web/resources/files/jquery-1.7.1.min.js',
	'./interfaces/web/resources/files/jquery-3.3.1.min.js',
	'./interfaces/web/resources/files/jquery.min.js',
	'./interfaces/web/resources/files/logo-icon.png',
	'./interfaces/web/resources/files/logo.png',
	# './interfaces/web/resources/files/xzero-rtl',
	],
),
('resources/files/fonts',
	['./interfaces/web/resources/files/fonts/amiri-quran-colored.eot',
	'./interfaces/web/resources/files/fonts/amiri-quran-colored.ttf',
	'./interfaces/web/resources/files/fonts/amiri-quran-colored.woff',
	'./interfaces/web/resources/files/fonts/DroidNaskh-Regular-Colored.ttf',
	'./interfaces/web/resources/files/fonts/DroidNaskh-Regular-Colored.woff',
	'./interfaces/web/resources/files/fonts/KacstOne.eot',
	'./interfaces/web/resources/files/fonts/KacstOne.otf',
	'./interfaces/web/resources/files/fonts/KacstOne.svg',
	'./interfaces/web/resources/files/fonts/KacstOne.ttf',
	'./interfaces/web/resources/files/fonts/KacstOne.woff',
	'./interfaces/web/resources/files/fonts/KacstOneColored.ttf',
	'./interfaces/web/resources/files/fonts/SimpleNaskhi-colores.ttf',
	]
), 
('resources/files/images',
	['./interfaces/web/resources/files/images/adawat.png',
	'./interfaces/web/resources/files/images/ayaspell.png',
	'./interfaces/web/resources/files/images/dreamdevdz.jpeg',
	'./interfaces/web/resources/files/images/main167-750x402.jpg',
	'./interfaces/web/resources/files/images/pyarabic.png',
	'./interfaces/web/resources/files/images/qutrub.jpg',
	'./interfaces/web/resources/files/images/radif.png',
	'./interfaces/web/resources/files/images/tashaphyne.png',

	]
),
('resources/files/samples',
	[
	'./interfaces/web/resources/files/samples/gotashkeel.png',
	'./interfaces/web/resources/files/samples/mishkal.png',
	'./interfaces/web/resources/files/samples/mishkal_alpha_smpl.png',
	'./interfaces/web/resources/files/samples/mixkal.jpg',
	]
),
## Todo
# ('resources/files/xzero-rtl',[]),
('resources/files/xzero-rtl/css',
	[
	'./interfaces/web/resources/files/xzero-rtl/css/bootstrap-arabic-theme.css',
	'./interfaces/web/resources/files/xzero-rtl/css/bootstrap-arabic-theme.css.map',
	'./interfaces/web/resources/files/xzero-rtl/css/bootstrap-arabic-theme.min.css',
	'./interfaces/web/resources/files/xzero-rtl/css/bootstrap-arabic.css',
	'./interfaces/web/resources/files/xzero-rtl/css/bootstrap-arabic.css.map',
	'./interfaces/web/resources/files/xzero-rtl/css/bootstrap-arabic.min.css',
	]
),
('resources/files/xzero-rtl/fonts',
	[
	'./interfaces/web/resources/files/xzero-rtl/fonts/glyphicons-halflings-regular.eot',
	'./interfaces/web/resources/files/xzero-rtl/fonts/glyphicons-halflings-regular.svg',
	'./interfaces/web/resources/files/xzero-rtl/fonts/glyphicons-halflings-regular.ttf',
	'./interfaces/web/resources/files/xzero-rtl/fonts/glyphicons-halflings-regular.woff',
	]
),
('resources/files/xzero-rtl/js',
	[
	'./interfaces/web/resources/files/xzero-rtl/js/bootstrap-arabic.js',
	'./interfaces/web/resources/files/xzero-rtl/js/bootstrap-arabic.min.js',
	]
),
('./interfaces/web/resources/templates',
	[ './interfaces/web/resources/templates/carousel.html',
	'./interfaces/web/resources/templates/contact.html',
	'./interfaces/web/resources/templates/doc.html',
	'./interfaces/web/resources/templates/download.html',
	'./interfaces/web/resources/templates/main.html',
	'./interfaces/web/resources/templates/projects.html',
	],
),

]; # end MyDataFiles
setup(name='Mishkal Software', version='1.5',
      description='Mishkal Software',
      author='Taha Zerrouki',
      author_email='taha.zerrouki@gmail.com',
      url='http://tahadz.com/mishkal',
      license='GPL',
	 windows = [
        {
            "script": "interfaces/gui/mishkal-gui.py",
            "icon_resources": [(1, "./interfaces/gui/ar/images/ix.ico")],
			
        }],
	console = [
		
        {
            "script": "bin/mishkal-console.py",
            "icon_resources": [(1, "./interfaces/gui/ar/images/ixn.ico")],
			
        }		
,
        {
            "script": "interfaces/web/mishkal-webserver.py",
            "icon_resources": [(1, "./interfaces/gui/ar/images/weblogo.ico")],
			
        }				
    ],
		# to avoid zipped file
		zipfile=None,
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
 
      data_files=MyDataFiles,
	 #end setup
 )