

mishkal
=======
  Mishkal Arabic text vocalization software
  
  Mishkal : Arabic text vocalization system
  
  مشكال لتشكيل النصوص العربية
  
  This program is licensed under the GPL License
  
  Developpers: 	Taha Zerrouki: http://tahadz.com
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
* file/directory	category	description 
* [program]
	- mishkal-console.py	program	Mishkal script used on shell command
	- mishkal-gui.py	program	launch mishkal GUI interface with QT
	- mishkal-webserver.py	web	lauch mishkal web server\n
  
* [docs]
  	docs/	docs	documentation
* [setup]
	- exe_setup.py	setup	prepare setup for windows using py2exe
  	- setup.py	setup	setup for library and linux package
* [mishkal]
  	- lib/aranasyn/		Arabic syntaxic analyzer
  	- lib/asmai/		Arabic syntaxic analyzer
  	- gui/		GUI source
  	- tashkeel/		Tashkeel module source
* core/		basic tools

* [lib]
  	- web/	lib	Libraries fot web interface
  	- web/okasha	trivial web framework
  	- web/paste		web frame work
  	- web/simplejson	simple json library		
* [data]
  	- data/	data	databases files
* [resouces]
  	- ar/	resources	reources for gui arabic
* [log]
  	- tmp/	log	tomporary fdirectory for web service
* [tools]
	- cleanpyc	setup	a shell script to remove .pyc files
* [test]
	- output/	test	test output
	- samples/	test	sample files
	- tools/	test	script to use mishkal
* [resources]
  	- files/	web	files used for web service
  	- templates/	web	Templates used for web service
  	- adawaty.py	web	a script for web service
  	- cgirunner.py	web	a script for web service using cgi
  	- crossdomain.xml	web	Configuration file to allow cross domain json API
  	- index.html	web	an index file to avoid directory access
  	- mishkal	web	A cgi Script used on web service
  	- mishkal-webserver.py	web	lauch mishkal web server
* [apps]
  	- mintiq	TTS	a shell script to join mishkla with espeak Text to speech

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
