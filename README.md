Mishkal
=======
  Mishkal Arabic text vocalization software  مشكال لتشكيل النصوص العربية

[![downloads]( https://img.shields.io/sourceforge/dt/mishkal.svg)](http://sourceforge.org/projects/mishkal)
[![downloads]( https://img.shields.io/sourceforge/dm/mishkal.svg)](http://sourceforge.org/projects/mishkal)

  Developpers: 	Taha Zerrouki: http://tahadz.com
	taha dot zerrouki at gmail dot com


Features |   value
---------|---------------------------------------------------------------------------------
Authors  | [Authors.md](https://github.com/linuxscout/mishkal/master/AUTHORS.md)
Release  | 1.10 Bouira
License  |[GPL](https://github.com/linuxscout/mishkal/master/LICENSE)
Tracker  |[linuxscout/mishkal/Issues](https://github.com/linuxscout/mishkal/issues)
Mailinglist  |[<mishkal@googlegroups.com>](http://groups.google.com/group/mishkal/)
Website  |[tahadz.com/mishkal](http://www.tahadz.com/mishkal/)
Source  |[Github](http://github.com/linuxscout/mishkal)
Download  |[sourceforge](http://mishkal.sourceforge.net)
Feedbacks  |[Comments](http://tahadz.com/mishkal/contact)
Accounts  |[@Facebook](https://www.facebook.com/mishkalarabic) [@Twitter](https://twitter.com/linuxscout)  [@Sourceforge](http://sourceforge.net/projectsmishkal/)

Setup
=====

### Debian/Ubuntu Linux

1. Install necessary packages:

```
sudo apt install git python-pip
python -m pip install pyarabic arramooz-pysqlite qalsadi tashaphyne mysam-tagmanager
```

2. Clone mishkal project from GitHub:

```
git clone https://github.com/linuxscout/mishkal.git
```

Usage
=====
### Windows :
 * Run MishkalGui.exe

### GUI: Linux
  - interfaces/gui/mishkal-gui.py

### Web server (linux, windows)
  * interfaces/web/mishkal-webserver
  * serving on 0.0.0.0:8080 view at http://127.0.0.1:8080
  * open in your browser the URL: http://127.0.0.1:8080

### Console (linux/windows)

 Usage: bin/mishkal-console -f filename [OPTIONS]


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
* file/directory	category	description 
* [bin]
	- mishkal-console.py	program	Mishkal script used on shell command
	- mishkal-gui.py	program	launch mishkal GUI interface with QT
	- mishkal-webserver.py	web	lauch mishkal web server\n
  
* [docs]
  	docs/	docs	documentation
* [setup]
	- exe_setup.py	setup	prepare setup for windows using py2exe
  	- setup.py	setup	setup for library and linux package
* [mishkal]
  	- tashkeel/		Tashkeel module source
* core/		basic API to join most of tools

* [support]
	- aranasyn	: syntaxical analyzer
	- arramooz	: arabic morphological dictionary
	- asmai		: semantic analyzer
	- CodernityDB :  pure python, fast, NoSQL database, used as cache system to minimize load of morphological analyzer 
	- collocations : collocation library ( deprecated)
	- libqutrub	: verb conjugation library used by morphological analyzer
	- maskouk	: collocation library
	- naftawayh	: word tag library
	- pyarabic	: basic arabic library
	- qalsadi	; morphological analyzer
	- spellcheck : spellchecking 
	- tashaphyne : light stemmer used by morphological analyzer


* [interfaces]
	* [web]
  	- lib/	lib	Libraries fot web interface
  	- lib/okasha	trivial web framework
  	- lib/paste		web frame work
  	- lib/simplejson	simple json library	
  	- files/	web	files used for web service
  	- templates/	web	Templates used for web service
  	- adawaty.py	web	a script for web service
  	- cgirunner.py	web	a script for web service using cgi
  	- crossdomain.xml	web	Configuration file to allow cross domain json API
  	- index.html	web	an index file to avoid directory access
  	- mishkal	web	A cgi Script used on web service
  	- mishkal-webserver.py	web	lauch mishkal web server
	* [gui]
	  	- ar/	resources	reources for gui arabic	
* [data]
  	- data/	data	databases files
* [log]
  	- tmp/	log	tomporary fdirectory for web service
* [tools]
	- cleanpyc	setup	a shell script to remove .pyc files
* [test]
	- output/	test	test output
	- samples/	test	sample files
	- tools/	test	script to use mishkal

* [apps]
  	- mintiq	TTS	a shell script to join mishkla with espeak Text to speech

How does Mishkal work:
----------------------
Mishkal use a rule based method to detect relations and diacritics,
First, it analyzes all morphological cases, it generates all possible diacritized word forms, by detecting all affixes and check it in a dictionary.
second, It add word frequency to each word.
The two previous steps are made by support/Qalsadi ( arabic morphological analyzer), the used dictionary is a separated project named 'Arramooz:  arabic dictionnary for morphology".
Third, we use a syntax analyzer  to detect all possible relations between words. The syntax library is named support/ArAnaSyn. This analyzer is basic for the moment, it use only linear relations between adjacent words.

Forth,  all data generated and relations will be analyzed semantically, to detect semantic relation in order to reduce ambiguity. The use libary is support/asmai ( Arabic semantic analysis). The semantic relations extraction is based on corpus. The used corpus is named "Tashkeela: arabic vocalized texts corpus".


In the final stage, The module mishkal/tashkeel tries to select the suitable word in the context,
it tries to get evidents cases, or more related cases, else, it tries to select more probable case, using some rules like select a stop word by default, or select Mansoub case by default.

The rest of program provides functions to handles interfaces and API with web/desktop or command line

JSON connection API:
-----------------

<a name="API"><h3>التشكيل عن بعد</h3></a>
يمكن استدعاء خدمة الموقع عبر مكتبة جيسون json و ajax من أي موقع، ويمكنك استعمالها في موقعك
طريقة الاستدعاء 
1- باستعمال تقنية  json مع مكتبة Jquery


<div dir='ltr'>
<!-- HTML generated using hilite.me --><div style="background: #ffffff; overflow:auto;width:auto;color:black;background:white;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%"> 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17</pre></td><td><pre style="margin: 0; line-height: 125%"><span style="color: #507090">&lt;!DOCTYPE html 	PUBLIC &quot;-//W3C//DTD XHTML 1.0 Transitional//EN&quot; &quot;http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd&quot;&gt;</span>
<span style="color: #007000">&lt;meta</span> <span style="color: #0000C0">http-equiv=</span><span style="background-color: #fff0f0">&quot;content-type&quot;</span> <span style="color: #0000C0">content=</span><span style="background-color: #fff0f0">&quot;text/html; charset=utf-8&quot;</span> <span style="color: #007000">/&gt;</span>
    <span style="color: #007000">&lt;script </span><span style="color: #0000C0">src=</span><span style="background-color: #fff0f0">&quot;http://code.jquery.com/jquery-latest.js&quot;</span><span style="color: #007000">&gt;&lt;/script&gt;</span>
<span style="color: #007000">&lt;/head&gt;</span>
<span style="color: #007000">&lt;body&gt;</span>
  <span style="color: #007000">&lt;div</span> <span style="color: #0000C0">id=</span><span style="background-color: #fff0f0">&quot;result&quot;</span><span style="color: #007000">&gt;</span>

<span style="color: #007000">&lt;/div&gt;</span>
<span style="color: #007000">&lt;script&gt;</span>
$().ready(<span style="color: #008000; font-weight: bold">function</span>() {
$.getJSON(<span style="background-color: #fff0f0">&quot;http://tahadz.com/mishkal/ajaxGet&quot;</span>, {text<span style="color: #303030">:</span><span style="background-color: #fff0f0">&quot;السلام عليكم\nاهلا بكم\nكيف حالكم&quot;</span>, action<span style="color: #303030">:</span><span style="background-color: #fff0f0">&quot;TashkeelText&quot;</span>},
  <span style="color: #008000; font-weight: bold">function</span>(data) {
      $(<span style="background-color: #fff0f0">&quot;#result&quot;</span>).text(data.result);
  });

 });
<span style="color: #007000">&lt;/script&gt;</span>
</pre></td></tr></table></div>

</div>



<br/>
الاستدعاء يكون كما يأتي
<!-- HTML generated using hilite.me --><div dir='ltr' style="background: #ffffff; overflow:auto;width:auto;color:black;background:white;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1</pre></td><td><pre style="margin: 0; line-height: 125%">$.getJSON(<span style="background-color: #fff0f0">&quot;http://tahadz.com/mishkal/ajax...&quot;</span>, {text<span style="color: #303030">:</span><span style="background-color: #fff0f0">&quot;السلام عليكم\nاهلا بكم\nكيف حالكم&quot;</span>, action<span style="color: #303030">:</span><span style="background-color: #fff0f0">&quot;TashkeelText&quot;</span>},
</pre></td></tr></table></div>

حيث<br/>
<ul>
<li><strong>text</strong>:  النص المطلوب تشكيله.</li>
<li><strong>action</strong>: العملية المطلوبة وهنا هي TashkeelText.</li>
</ul>
النتيجة تكون من الشكل
<pre dir="ltr">
<!-- HTML generated using hilite.me --><div dir='ltr' style="background: #ffffff; overflow:auto;width:auto;color:black;background:white;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1</pre></td><td><pre style="margin: 0; line-height: 125%">{<span style="color: #007000">&quot;result&quot;</span>: <span style="background-color: #fff0f0">&quot; السّلامُ عَلَيكُمْ اهلا بِكُمْ كَيْفَ حالُكُمْ&quot;</span>, <span style="color: #007000">&quot;order&quot;</span>: <span style="background-color: #fff0f0">&quot;0&quot;</span>}
</pre></td></tr></table></div>

</pre>
حيث
<ul>
<li><strong>result</strong>: النص الناتج المشكول.</li>
<li><strong>order</strong>: رقم السطر في النص الأصلي، فإذا كان النص الأصلي كبيرا يقسمه المشكال لعدد من الاسطر، وقد لا يرجعون في نفس الترتيب، لذا حددنا رقم الترتيب.</li>
</ul>


## Featured Posts
-  “مشكال” لتشكيل النصوص العربية بإحترافية  [كمال فودة](http://www.prameg2day.com/?p=5194)
-  كيفيشكيل الحروف والكلمات أو حتى نصوص باللغة العربية في ثواني من خلال متصفحك-  [رضا بوربعة](http://www.th3professional.com/2015/09/blog-post_36.html)
-  خدمة عربية جديدة : تشكيل النصوص العربية [Sam Hamou](http://3-arabi.blogspot.com/2015/05/mishkal-arabic-3arabi.html)
-  إطلاق الإصدار التجريبي برنامج مشكال لتشكيل النصوص العربية
[Zaid AlSaadi](http://itwadi.com/node/2184)
- مشكال: الطريق نحو التشكيل [مدونة اليراع](https://tahadz.wordpress.com/2011/07/08/mishkal00/)
-  مشكال لتشكيل النصوص العربية: إطلاق واجهة سطح المكتب [مدونة اليراع](https://tahadz.wordpress.com/2012/01/07/mishkaldesktop/)
- تعرّف على مشاريع “تحدّث” .. مشاريعٌ للغةٍ عظيمة [محمد هاني صباغ](http://www.arageek.com/tech/2014/11/28/tahdz-new-services-for-arabic-writing.html)

