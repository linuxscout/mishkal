Mishkal
=======

Mishkal Arabic text vocalization software مشكال لتشكيل النصوص العربية


Developpers: Taha Zerrouki: http://tahadz.com taha dot zerrouki at gmail
dot com

+---------+------------------------------------------------------------------+
| Feature | value                                                            |
| s       |                                                                  |
+=========+==================================================================+
| Authors | `Authors.md <https://github.com/linuxscout/mishkal/master/AUTHOR |
|         | S.md>`__                                                         |
+---------+------------------------------------------------------------------+
| Release | 1.10 Bouira                                                      |
+---------+------------------------------------------------------------------+
| License | `GPL <https://github.com/linuxscout/mishkal/master/LICENSE>`__   |
+---------+------------------------------------------------------------------+
| Tracker | `linuxscout/mishkal/Issues <https://github.com/linuxscout/mishka |
|         | l/issues>`__                                                     |
+---------+------------------------------------------------------------------+
| Mailing | ` <http://groups.google.com/group/mishkal/>`__                   |
| list    |                                                                  |
+---------+------------------------------------------------------------------+
| Website | `tahadz.com/mishkal <http://www.tahadz.com/mishkal/>`__          |
+---------+------------------------------------------------------------------+
| Source  | `Github <http://github.com/linuxscout/mishkal>`__                |
+---------+------------------------------------------------------------------+
| Downloa | `sourceforge <http://mishkal.sourceforge.net>`__                 |
| d       |                                                                  |
+---------+------------------------------------------------------------------+
| Feedbac | `Comments <http://tahadz.com/mishkal/contact>`__                 |
| ks      |                                                                  |
+---------+------------------------------------------------------------------+
| Account | [@Facebook](https://www.facebook.com/mishkalarabic)              |
| s       | [@Twitter](https://twitter.com/linuxscout)                       |
|         | [@Sourceforge](http://sourceforge.net/projectsmishkal/)          |
+---------+------------------------------------------------------------------+

Citation
--------

.. code:: bibtex

    @thesis{zerrouki2020adawat,
    author = {Taha Zerrouki},
    title = {Towards An Open Platform For Arabic Language Processing},
    type = {PhD thesis},
    institution = {Ecole Nationale Supérieure d'informatique, Alger, Algérie},
    date = {2020},
    }

Install
-------

You can Install Mishkal as library or Software ### Python lib

::

    pip install mishkal

Install from github
~~~~~~~~~~~~~~~~~~~

1. Clone mishkal project from GitHub:

::

    git clone https://github.com/linuxscout/mishkal.git

2. Install necessary packages:

::

    pip install -r miskal/requirements.txt

requirments
^^^^^^^^^^^

::

    - pyarabic  : basic arabic library
    - sylajone  : aranasyn syntaxical analyzer
    - arramooz  : arabic morphological dictionary
    - asmai     : semantic analyzer
    - CodernityDB :  pure python, fast, NoSQL database, used as cache system to minimize load of morphological analyzer 
    - collocations : collocation library ( deprecated)
    - libqutrub : verb conjugation library used by morphological analyzer
    - maskouk   : collocation library
    - naftawayh : word tag library
    - qalsadi   ; morphological analyzer
    - tashaphyne : light stemmer used by morphological analyzer

Usage
-----

Mishkal provides:

-  Console command line
-  python library
-  GUi interface
-  Web interface
-  API interface ### GUI:
-  Windows: ``MishkalGui.exe``

-  GUI: Linux ``python interfaces/gui/mishkal-gui.py`` ### Web server
   (linux, windows) ``python3 interfaces/web/mishkal-webserver``

-  serving on 0.0.0.0:8080 view at http://127.0.0.1:8080
-  open in your browser the URL: http://127.0.0.1:8080

Console (linux/windows)
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    $ python3 bin/mishkal-console.py -f filename

    Usage: bin/mishal-console.py  -f filename [OPTIONS]
               bin/mishal-console.py  'السلام عليكم' [OPTIONS]

            [-f | --file = filename]       input file 
            [-o | --outfile = filename]    output file to write vocalized text to, '$FILENAME (Tashkeel).txt' by default
            
            [-h | --help]             outputs this usage message
            [-v | --version]        program version
            [-p | --progress]      display progress status
            [-a | --verbose]       enable verbosity

            * Tashkeel Actions
            -------------------
            [-r | --reduced]        Reduced Tashkeel.
            [-s | --strip]             Strip tashkeel (remove harakat).
            [-c | --compare]      compare the vocalized text with the program output

            * Tashkeel Options
            ------------------
            [-l | --limit]             vocalize only a limited number of line
            [-x | --syntax]         disable syntaxic analysis
            [-m | --semantic]    disable semantic analysis
            [-g | --train]             enable training option
            [-i | --ignore]           ignore the last Mark on output words.
            [-t | --stat]               disable statistic tashkeel

    This program is licensed under the GPL License

Library
~~~~~~~

.. code:: shell

    pip install mishkal

example:
^^^^^^^^

.. code:: python

    >>> import mishkal.tashkeel
    >>> vocalizer = mishkal.tashkeel.TashkeelClass()
    >>> text = u"تطلع الشمس صباحا"
    >>> vocalizer.tashkeel(text)
    ' تَطْلُعُ الشَّمْسُ صَبَاحًا'
    >>> 

JSON connection API التشكيل عن بعد
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

يمكن استدعاء خدمة الموقع عبر مكتبة جيسون json و ajax من أي موقع، ويمكنك
استعمالها في موقعك. \* طريقة الاستدعاء 1- باستعمال تقنية json مع مكتبة
Jquery

.. code:: javascript

    <!DOCTYPE html   PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <script src="http://code.jquery.com/jquery-latest.js"></script>
    </head>
    <body>
      <div id="result">

    </div>
    <script>
    $().ready(function() {
    $.getJSON("http://tahadz.com/mishkal/ajaxGet", {text:"السلام عليكم\nاهلا بكم\nكيف حالكم", action:"TashkeelText"},
      function(data) {
          $("#result").text(data.result);
      });

     });
    </script>

الاستدعاء يكون كما يأتي

.. code:: javascript

    $.getJSON("http://tahadz.com/mishkal/ajax...", {text:"السلام عليكم\nاهلا بكم\nكيف حالكم", action:"TashkeelText"},

حيث

-  **text**: النص المطلوب تشكيله.
-  **action**: العملية المطلوبة وهنا هي TashkeelText.

النتيجة تكون من الشكل

.. code:: javascript

    {"result": " السّلامُ عَلَيكُمْ اهلا بِكُمْ كَيْفَ حالُكُمْ", "order": "0"}

حيث

-  **result**: النص الناتج المشكول.
-  **order**: رقم السطر في النص الأصلي، فإذا كان النص الأصلي كبيرا يقسمه
   المشكال لعدد من الاسطر، وقد لا يرجعون في نفس الترتيب، لذا حددنا رقم
   الترتيب.

How does Mishkal work:
----------------------

Mishkal use a rule based method to detect relations and diacritics,
First, it analyzes all morphological cases, it generates all possible
diacritized word forms, by detecting all affixes and check it in a
dictionary. second, It add word frequency to each word.

The two previous steps are made by support/Qalsadi ( arabic
morphological analyzer), the used dictionary is a separated project
named 'Arramooz: arabic dictionnary for morphology".

Third, we use a syntax analyzer to detect all possible relations between
words. The syntax library is named support/ArAnaSyn. This analyzer is
basic for the moment, it use only linear relations between adjacent
words.

Forth, all data generated and relations will be analyzed semantically,
to detect semantic relation in order to reduce ambiguity. The use libary
is support/asmai ( Arabic semantic analysis). The semantic relations
extraction is based on corpus. The used corpus is named "Tashkeela:
arabic vocalized texts corpus".

In the final stage, The module mishkal/tashkeel tries to select the
suitable word in the context, it tries to get evidents cases, or more
related cases, else, it tries to select more probable case, using some
rules like select a stop word by default, or select Mansoub case by
default.

The rest of program provides functions to handles interfaces and API
with web/desktop or command line

Featured Posts
--------------

-  “مشكال” لتشكيل النصوص العربية بإحترافية `كمال
   فودة <http://www.prameg2day.com/?p=5194>`__
-  كيفية شكيل الحروف والكلمات أو حتى نصوص باللغة العربية في ثواني من
   خلال متصفحك- `رضا
   بوربعة <http://www.th3professional.com/2015/09/blog-post_36.html>`__
-  خدمة عربية جديدة : تشكيل النصوص العربية `Sam
   Hamou <http://3-arabi.blogspot.com/2015/05/mishkal-arabic-3arabi.html>`__
-  إطلاق الإصدار التجريبي برنامج مشكال لتشكيل النصوص العربية `Zaid
   AlSaadi <http://itwadi.com/node/2184>`__
-  مشكال: الطريق نحو التشكيل `مدونة
   اليراع <https://tahadz.wordpress.com/2011/07/08/mishkal00/>`__
-  مشكال لتشكيل النصوص العربية: إطلاق واجهة سطح المكتب `مدونة
   اليراع <https://tahadz.wordpress.com/2012/01/07/mishkaldesktop/>`__
-  تعرّف على مشاريع “تحدّث” .. مشاريعٌ للغةٍ عظيمة `محمد هاني
   صباغ <http://www.arageek.com/tech/2014/11/28/tahdz-new-services-for-arabic-writing.html>`__

