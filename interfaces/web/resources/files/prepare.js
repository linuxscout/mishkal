var random_click = function(e) {
    e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: '',
      action: "RandomText"
    }, function(data) {
      if (data) document.NewForm.InputText.value = data.result;
      else document.NewForm.InputText.value = "TZA";
    });
  }

var stripharakat_click = function(e) {
        e.preventDefault();
    //  $("#result").html("<pre>TATAH\nNTATAH</pre>");
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "StripHarakat"
    }, function(d) {
      $("#result").html("<p>" + d.result + "</p>");
      //"#result").text(d.time);
    });
  }
  
var csv2data_click = function(e) {
        e.preventDefault();
    $.getJSON(script + ")s/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "CsvToData"
    }, function(d) {
      $("#result").html("<pre>" + d.result + "</pre>");
      //"#result").text(d.time);
    });
  }

//--------------------------------------
var number_click = function() {
      e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "NumberToLetters"
    }, function(d) {
      $("#result").html("<p>" + d.result + "</p>");
      //"#result").text(d.time);
    });
  }
  
  
  // extact named enteties 
var named_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "extractNamed"
    }, function(d) {
      $("#result").html("<p>" + d.result + "</p>");
      //"#result").text(d.time);
    });
  }
  
  // extact numbers enteties 
var numbred_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "extractNumbered"
    }, function(d) {
      $("#result").html("<p>" + d.result + "</p>");
      //"#result").text(d.time);
    });
  }

  // extact enteties 
var extractEnteties_click = function(e) {
      e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "extractEnteties"
    }, function(d) {
      $("#result").html(d.result +"<br/><hr/><span class='coll'>متلازمات</span> <span class='named'>مسميات</span> <span class='number'>معدودات</span> ");
      
    });
  }

//----------Tabs----------------------  
var more_click = function(e) {
      e.preventDefault();
    $("#moresection").slideToggle();
  }

  var vocalize_group_click = function(e) {
        e.preventDefault();
    $("#vocalizesection").slideToggle();
    $("#moresection").hide();
  }
  //Unshape text 
  var unshape_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Unshape"
    }, function(d) {
      $("#result").html("<p>" + d.result + "</p>");
    });
  }
  //move result into input 
  var move_click = function(e) {
        e.preventDefault();
    $(".txkl").change();
    document.NewForm.InputText.value = $("#result").text();
  }
  //copy result into clipboard
  var copy_click = function(e) {
        e.preventDefault();
    $(".txkl").change();
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($("#result").text()).select();
    document.execCommand("copy");
    $temp.remove();
    //document.NewForm.InputText.value = $("#result").text();
  }


// morphology analysis by Al-Qalsadi
  var stem_click = function(e) {
        e.preventDefault();
    $("#loading").slideDown();
    var $table = $('<table/>');
    var table = $table.attr("border", "1")[0];
    var headers = ["<tr>", "<th>المدخل</th>", "<th>تشكيل</th>", "<th>الأصل</th>",
      "<th>الزوائد</th>", "<th>الجذع</th>",
      "<th style='white-space:nowrap;'>الحالة الإعرابية</th>",
      "<th>النوع</th><th>النحوي</th>", "<th>شيوع</th>", "</tr>"
    ].join('');
    $table.append(headers);
    var item = "";
    $("#result").html("");
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "LightStemmer"
    }, function(d) {
      for (k in d.result) {
        var tbody = document.createElement('tbody');
        if (d.result[k].length == 0) {
          var tr = document.createElement('tr');
          var td = document.createElement('td');
          td.appendChild(document.createTextNode(k));
          tr.appendChild(td);
          for (j = 0; j < 7; j++) {
            var td = document.createElement('td');
            td.appendChild(document.createTextNode("-"));
            tr.appendChild(td);
          }
          tbody.appendChild(tr);
        } else {
          for (i = 0; i < d.result[k].length; i++) {
            var tr = document.createElement('tr');
            item = d.result[k][i];
            var td = document.createElement('td');
            td.appendChild(document.createTextNode(item['word']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['vocalized']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['original']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['affix']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['stem']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['tags'].replace(/:/g, ': ')));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['type']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(JSON.stringify(item['syntax'])));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['freq']));
            tr.appendChild(td);
            tbody.appendChild(tr);
          }
        }
        table.appendChild(tbody);
      }
      $("#result").append($table);
    });
    $("#loading").slideUp();
  }
  var tokenize_click = function(e) {
        e.preventDefault();
    var item;
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Tokenize"
    }, function(d) {
      $("#result").html("");
      for (i = 0; i < d.result.length; i++) {
        $("#result").append(d.result[i] + "<br/>");
      }
    });
  }
// Gramatical Analysis
 var synt_click = function(e) {
       e.preventDefault();
    $("#loading").slideDown();
    var $table = $('<table/>');
    var table = $table.attr("border", "1")[0];
    var headers = ["<tr>", "<th>المدخل</th>", "<th>تشكيل</th>", "<th>الأصل</th>",
      "<th>الزوائد</th>", "<th>الجذع</th>",
      "<th style='white-space:nowrap;'>الحالة الإعرابية</th>",
      "<th>النوع</th><th>النحوي</th>", "<th>شيوع</th>", "</tr>"
    ].join('');
    $table.append(headers);
    var item = "";
    $("#result").html("");
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "LightStemmer"
    }, function(d) {
        draw_graph(d);
      for (k in d.result) {

        var tbody = document.createElement('tbody');
        if (d.result[k].length == 0) {
          var tr = document.createElement('tr');
          var td = document.createElement('td');
          td.appendChild(document.createTextNode(k));
          tr.appendChild(td);
          for (j = 0; j < 7; j++) {
            var td = document.createElement('td');
            td.appendChild(document.createTextNode("-"));
            tr.appendChild(td);
          }
          tbody.appendChild(tr);
        } else {
          for (i = 0; i < d.result[k].length; i++) {
            var tr = document.createElement('tr');
            item = d.result[k][i];
            var td = document.createElement('td');
            td.appendChild(document.createTextNode(item['word']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['vocalized']));
            tr.appendChild(td);
            //~td = document.createElement('td');
            //~td.appendChild(document.createTextNode( item['semivocalized']) );
            //~tr.appendChild(td);      
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['original']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['affix']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['stem']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['tags'].replace(/:/g, ': ')));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['type']));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(JSON.stringify(item['syntax'])));
            tr.appendChild(td);
            td = document.createElement('td');
            td.appendChild(document.createTextNode(item['freq']));
            tr.appendChild(td);
            tbody.appendChild(tr);
          }
        }
        table.appendChild(tbody);
      }
      $("#result").append($table);
    });
    $("#loading").slideUp();
  }  
  
  // extract chunks from text
    var chunk_click = function(e) {
          e.preventDefault();
    var item;
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "chunk"
    }, function(d) {
      $("#result").html("");
      for (i = 0; i < d.result.length; i++) {
        $("#result").append(d.result[i] + "<br/>");
      }
    });
  }
  
    // extract chunks from text
    var bigrams_click = function(e) {
          e.preventDefault();
    var item;
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "bigrams"
    }, function(d) {
      $("#result").html("");
      for (i = 0; i < d.result.length; i++) {
        $("#result").append(d.result[i] + "<br/>");
      }
    });
  }
  // inverse order
  var inverse_click = function(e) {
        e.preventDefault();
    var item;
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Inverse"
    }, function(d) {
      $("#result").html("");
      for (i = 0; i < d.result.length; i++) {
        $("#result").append(d.result[i] + "<br/>");
      }
    });
  }
  // Ajust an Arabic poetry in two columns  
  var poetry_click = function(e) {
        e.preventDefault();
    var $table = $('<table/>');
    var table = $table.attr("border", "0")[0];
    //$table.attr("width", '600');
    $table.addClass('poetryJustifyCSS3');
    //$table.attr( "style",'text-align: justify; text-justify: newspaper; text-kashida-space: 100;”);
    //var headers = ["<tr>", "<th>الصدر</th>", "<th>العجز</th>", "</tr>"].join('');
    //$table.append(headers);
    var item;
    $("#result").html("");
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Poetry"
    }, function(d) {
      for (i = 0; i < d.result.length; i++) {
        var tr = document.createElement('tr');
        item = d.result[i];
        var td = document.createElement('td');
        td.appendChild(document.createTextNode(item[0]));
        tr.appendChild(td);
        td = document.createElement('td');
        td.appendChild(document.createTextNode(item[1]));
        tr.appendChild(td);
        table.appendChild(tr);
      }
      $("#result").append($table);
    });
  }
  var romanize_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Romanize"
    }, function(d) {
      $("#result").html("<p>" + d.result + "</p>");
    });
  }
  var contribute_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: $("#result").text(),
      action: "Contribute"
    }, function(d) {
      alert(d.result);
    });
  }
  // normalize text
  var normalize_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Normalize"
    }, function(d) {
      $("#result").html(d.result);
    });
  }
  var wordtag_click = function(e) {
        e.preventDefault();
    var $table = $('<table/>');
    var $div = $('<div/>');
    var div = $div[0];
    var table = $table.attr("border", "0")[0];
    $table.attr("width", '600');
    //$table.attr( "style",'text-align: justify; text-justify: newspaper; text-kashida-space: 100;”);
    var headers = ["<tr>", "<th>الكلمة</th>", "<th>تصنيفها</th>", "</tr>"].join('');
    $table.append(headers);
    $("#result").html("");
    var item;
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Wordtag"
    }, function(d) {
      $("#result").html("");
      for (i = 0; i < d.result.length; i++) {
        item = d.result[i];
        var span = document.createElement('span');
        span.setAttribute('class', item.tag);
        span.appendChild(document.createTextNode(" " + item.word));
        div.appendChild(span);
        //display as table
        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.appendChild(document.createTextNode(item.word));
        tr.appendChild(td);
        td = document.createElement('td');
        td.setAttribute('class', item.tag);
        td.appendChild(document.createTextNode(item.tag));
        tr.appendChild(td);
        table.appendChild(tr);
      }
      $("#result").append($div);
      $("#result").append($table);
    });
  }
  var language_click = function(e) {
        e.preventDefault();
    var $div = $('<div/>');
    var div = $div[0];
    $("#result").html("");
    var item;
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Language"
    }, function(d) {
      $("#result").html("");
      for (i = 0; i < d.result.length; i++) {
        item = d.result[i];
        var span = document.createElement('span');
        span.setAttribute('class', item[0]);
        span.appendChild(document.createTextNode(item[1]));
        div.appendChild(span);
      }
      $("#result").append($div);
    });
  }


  // generate all affixation form of a word  
  var affixate_click = function(e) {
        e.preventDefault();
    var $table = $('<table/>');
    var table = $table.attr("border", "0")[0];
    $table.attr("width", '600');
    //$table.attr( "style",'text-align: justify; text-justify: newspaper; text-kashida-space: 100;”);
    var headers = ["<tr>", "<th>الكلمة</th>", "<th>تقطيعها</th>", "</tr>"].join('');
    $table.append(headers);
    $("#result").html("");
    var item;
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Affixate"
    }, function(d) {
      $("#result").html("");
      for (i = 0; i < d.result.length; i++) {
        var tr = document.createElement('tr');
        item = d.result[i];
        var td = document.createElement('td');
        td.appendChild(document.createTextNode(item.standard));
        tr.appendChild(td);
        td = document.createElement('td');
        td.appendChild(document.createTextNode(item.affixed));
        tr.appendChild(td);
        table.appendChild(tr);
        //      $("#result").append(+"  "++"<br/>" );
      }
      $("#result").append($table);
    });
  }

  var tashkeel2_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: ocument.NewForm.InputText.value,
      action: "Tashkeel"
    }, function(d) {
      $("#result").html("<div class=\'tashkeel\'>" + d.result + "</div>");
      $("#contributeSection").show();
    });
  }
  var reducetashkeel_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "ReduceTashkeel"
    }, function(d) {
      $("#result").html("<div class=\'tashkeel\'>" + d.result + "</div>");
      $("#contributeSection").show();
    });
  }
  var comparetashkeel_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "CompareTashkeel"
    }, function(d) {
      var table = d.result;
      $("#result").html("<div class=\'tashkeel\'>" + table + "</div>");
    });
  }
  var showCollocations_click = function(e) {
        e.preventDefault();
    $.getJSON(script + "/ajaxGet", {text: document.NewForm.InputText.value,
      action: "showCollocations"
    }, function(d) {$("#result").html(d.result);});
  }
  $('.txkl').select(function() {
    $(".txkl").change();
  }
  var tashkeel_click = function(e) {
    var collocation = 1;
    var vocalizewWordsEnds = "0";
    if (document.NewForm.LastMark.checked == 1) vocalizewWordsEnds = "1";
    var inputText = document.NewForm.InputText.value;
    inputText = inputText.replace(/(\.+)/g, "\$1\n");
    // replace all spaces to save it in the output
    var textlistOne = inputText.split('\n');
   $("#loading").hide();    
    $("#result").html("");
    $("#loading").show();
    $('#loading').data('length', 0);
    
    var textlist = new Array();
    for (var i = 0; i < textlistOne.length; i++) {
      if (textlistOne[i] != "") textlist.push(textlistOne[i]);
    }
    $('#loading').data('length', textlist.length);
    for (var i = 0; i < textlist.length; i++) {
      // split inputtext into lines and clauses
      // add dots to save the phrases number.
      $("#loading").html($("#loading").html() + ".");
      $.getJSON(script + "/ajaxGet", {
        text: textlist[i],
        action: "Tashkeel2",
        order: i.toString(),
        lastmark: vocalizewWordsEnds
      }, function(d) {
        console.log(d);
        // Grammar graph 
        //draw_graph();
        var text = "";
        var id = parseInt(d.order);
        var openColocation = 0;
        for (var i = 0; i < d.result.length; i++) {
          
          item = d.result[i];
          var currentId = id * 100 + i;
          if (item.chosen.indexOf("~~") >= 0) { // handle collocations
            openColocation = 0;
            text += "</span><span class='collocation' title='دقّق تشكيل هذه العبارة'>" +
              item.chosen.replace("~~", "");
          } else if (item.chosen.indexOf("~") >= 0) { // handle collocations
            if (openColocation == 0) {
              openColocation = 1;
              text += item.chosen.replace("~", "") +
                " <span class='collocation' title='دقّق تشكيل هذه العبارة'>";
            } else {
              openColocation = 0;
              text += "</span>" + item.chosen.replace("~", "");
            }
          } else {
            var pattern = /[-[\]{}()*+?.,،:\\^$|#\s]/;
            if (!pattern.test(item.chosen)) text += " ";
            var word_to_display = item.chosen;
            if (document.NewForm.LastMark.checked == 0) word_to_display = item.semi;
            text += "<span class='vocalized' id='" + currentId + "' inflect='" + item.inflect.replace(/:+/g, ', ') +
              "' suggest='" + item.suggest.replace(/;/g, '، ') + "' rule='" + item.rule +
              "' link='" + item.link + "'>" + word_to_display + "</span>";
            //~ $('#result').data(currentId.toString(), item.suggest);
            $('#result').data(currentId.toString(), item);
          }
        }
        // display the result
        $("#loading").data(d.order, text);
        $("#result").html($("#result").html() + "<div class=\'tashkeel\'>" + text +
          "</div>");
        // dela dot, to count the phrase executed
        $("#loading").html($("#loading").html().replace('.', ''));
        if ($("#loading").html().indexOf('.') < 0) { // if no dot, the work is terminated
          // redraw the text result with order
          var ordredtext = "";
          for (var j = 0; j < $("#loading").data('length'); j++) {
            ordredtext += $("#loading").data(j.toString());
          }
            $('#result').data("count",d.result.length);
            $('#result').html("<div class=\'tashkeel\'>" + ordredtext + "</div>");
            $("#loading").hide();
        }
      });
    } // end for i intextlist
    $("#contributeSection").show();
  }
  

  $('.vocalized').live("click", function() {
    $(".txkl").change();
    var myword = $(this);
    var nextword = $(this).next();
    var id = myword.attr('id');
    var list = $("#result").data(id).suggest.split(';');
    //~ var text = "<form><select class='txkl' id='" + id + " size=3'>";
    var text = "<select class='txkl' id='" + id + "'>";
    var cpt = 0;
    for (i in list) {
      if (list[i] != "") {
        if (myword.text() != list[i]) text += "<option>" + list[i] + "</option>";
        else text += "<option selected=" + list[i] + ">" + list[i] + "</option>";
        cpt += 1;
      }
    }
    text += "<option><strong>تعديــل...</strong></option>";
    text += "</select>";
    if (cpt > 1) {
      myword.replaceWith(text);

    } else {
      text = "<input type='text' class='txkl'  size='10' id='" + myword.attr('id') +
        "' value='" + myword.text() + "'/>";
      myword.replaceWith(text);
    }
    console.log(myword.text()+";;"+nextword.text())
});
  $('.txkl').live('change', function() {
    if ($(this).val() != "تعديــل...") {
      var item = $("#result").data($(this).attr('id'));
      //~ var text = "<span class='vocalized' id='" + $(this).attr('id') + "'>" + $(this).val() +
        //~ "</span>";
     $
      var text = "<span class='vocalized' id='" + $(this).attr('id') + "' suggest='" + item.suggest.replace(/;/g, '، ') +
         "' inflect='معدّل يدويا'rule='معدّل يدويا' link='N/A' >" + $(this).val() + "</span>";
      $(this).replaceWith(text);
    } else // case of editing other choice
    {
      var list = $("#result").data($(this).attr('id')).suggest.split(';');
      text = "<input type='text' class='txkl'  size='10' id='" + $(this).attr('id') +
        "' value='" + list[0] + "'/>";
      $(this).replaceWith(text);
       console.log($(this).text()+"-"+$(this).next().text());
    }
 }
  $('.spld').live('change', function() {
    if ($(this).val() != "تعديــل...") {
      var text = "<span class='spld' id='" + $(this).attr('id') + "'>" + $(this).val() +
        "</span>";
      $(this).replaceWith(text);
    } else // case of editing other choice
    {
      var list = $("#result").data($(this).attr('id')).suggest.split(';');
      var text = "<input type='text' class='spld'  size='10' id='" + $(this).attr('id') +
        "' value='" + list[0] + "'/>";
      $(this).replaceWith(text);
       console.log($(this).text()+"-"+$(this).next().text());
    }
 }
  // spell checking
  var spellcheck_click = function(e) {
    var collocation = 1;
    var vocalizewWordsEnds = "0";
    if (document.NewForm.LastMark.checked == 1) vocalizewWordsEnds = "1";
    var inputText = document.NewForm.InputText.value;
    inputText = inputText.replace(/(\.+)/g, "\$1\n");
    // replace all spaces to save it in the output
    // in order to keep the same typography 
    var textlistOne = inputText.split('\n');
    $("#result").html("");
    $("#loading").show();
    $('#loading').data('length', 0);
    var textlist = new Array();
    for (var i = 0; i < textlistOne.length; i++) {
      if (textlistOne[i] != "") textlist.push(textlistOne[i]);
    }
    $('#loading').data('length', textlist.length);
    for (var i = 0; i < textlist.length; i++) {
      // split inputtext into lines and clauses
      // add dots to save the phrases number.
      $("#loading").html($("#loading").html() + ".");
      $.getJSON(script + "/ajaxGet", {
        text: textlist[i],
        action: "SpellCheck",
        order: i.toString(),
        lastmark: vocalizewWordsEnds
      }, function(d) {
        console.log(d);
        var text = "";
        var id = parseInt(d.order);
        var openColocation = 0;
        for (var i = 0; i < d.result.length; i++) {
          item = d.result[i];
          var currentId = id * 100 + i;
          //text+=currentId.toString();
          if (item.chosen.indexOf("~~") >= 0) { // handle collocations
            openColocation = 0;
            text += "</span><span class='collocation' title='دقّق تشكيل هذه العبارة'>" +
              item.chosen.replace("~~", "");
          } else if (item.chosen.indexOf("~") >= 0) { // handle collocations
            if (openColocation == 0) {
              openColocation = 1;
              text += item.chosen.replace("~", "") +
                " <span class='collocation' title='دقّق تشكيل هذه العبارة'>";
            } else {
              openColocation = 0;
              text += "</span>" + item.chosen.replace("~", "");
            }
          } else {
            var pattern = /[-[\]{}()*+?.,،:\\^$|#\s]/;
            if (!pattern.test(item.chosen)) text += " ";
            if (item.suggest != '') text += "<span class='spelled-incorrect' id='" +
              currentId + "'>" + item.chosen + "</span>";
            else text += "<span class='spelled' id='" + currentId + "'>" + item.chosen +
              "</span>";
            $('#result').data(currentId.toString(), item.suggest);
          }
        }
        // display the result
        $("#loading").data(d.order, text);
        $("#result").html($("#result").html() + "<p class=\'spellStyle\'>" + text +
          "</p>");
        // dela dot, to count the phrase executed
        $("#loading").html($("#loading").html().replace('.', ''));
        if ($("#loading").html().indexOf('.') < 0) { // if no dot, the work is terminated
          // redraw the text result with order
          var ordredtext = "";
          for (var j = 0; j < $("#loading").data('length'); j++) {
            ordredtext += "<br/>" + $("#loading").data(j.toString());
          }
          $('#result').html("<p class=\'spellStyle\'>" + ordredtext + "</p>");
          $("#loading").hide();
        }
      });
    } // end for i intextlist
    $("#contributeSection").show();
  }
  
  $('.spelled-incorrect').live("click", function() {
    $(".spld").change();
    var myword = $(this);
    var id = myword.attr('id');
    var list = $("#result").data(id).split(';');
    var text = "<select class='spld' id='" + id + "'>";
    var cpt = 0;
    for (i in list) {
      if (list[i] != "") {
        if (myword.text() != list[i]) text += "<option>" + list[i] + "</option>";
        else text += "<option selected=" + list[i] + ">" + list[i] + "</option>";
        cpt += 1;
      }
    }
    text += "<option><strong>تعديــل...</strong></option>";
    text += "</select>";
    // disable others suggestion lists  
    if (cpt > 1) {
      myword.replaceWith(text);
    } else {
      text = "<input type='text' class='spld'  size='10' id='" + myword.attr('id') +
        "' value='" + myword.text() + "'/>";
      myword.replaceWith(text);
    }
  });
  // change diff 
  $('#diff').live("hover", function() {
    var text = $(this).text() + " : " + $(this).attr('original') + "<br/>"+$(this).attr('inflect')  + "<br/>ق[" + $(this).attr('rule') + "] " + $(this).attr('link') ;
    if ($('#result').data("count")>20) {$('#hint').html(text);  $('#hint').show(); $('#small_hint').hide();}
    else  {$('#small_hint').html(text); $('#small_hint').show();$('#hint').hide();}

  });
  // change diff 
  $('#diff').live("mouseleave", function() {
    $('#small_hint').html("");
    $('#small_hint').hide();
  });
  // display infos on vocalized  
  $('.vocalized').live("hover", function(e) {
    var text = $(this).text() + " : " + $(this).attr('inflect')  + "<br/>ق[" + $(this).attr('rule') + "] " + $(this).attr('link') + "<br/>" + $(this).attr('suggest');
    if ($('#result').data("count")>20) {$('#hint').html(text);  $('#hint').show(); $('#small_hint').hide();}
    else  {$('#small_hint').html(text); $('#small_hint').show();$('#hint').hide();}
  });
  // change diff 
  $('.vocalized').live("mouseleave", function() {
    $('#hint').hide("");
    $('#small_hint').hide("");
  });
});
