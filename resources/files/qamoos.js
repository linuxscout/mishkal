var $db=$("#db"),$tbody=$("#results"),$btn=$("#btn"),$ld=$("#loading"),$err=$("#error");
  function WordClick(text)
  {
  document.myForm.word.value=text;
  $btn.click();
  }
$().ready(function() {
  $().ajaxError(function(d) { $ld.slideUp(); $err.slideDown(); });

  $btn.click(
  function() {
  w=document.myForm.word.value;
  lang=document.myForm.lang.value;
  db=document.myForm.db.value;
  $err.hide();
  $ld.slideDown();
  $.getJSON(script+"/search", {w:w,lang:lang,db:db}, function(d){
    $tbody.html("");
    for (var i in d){
      $tr=$("<tr/>").appendTo($tbody);
     // $("<td/>").text(d[i].ar).appendTo($tr);
	 var mywordlink="<a id='action' onClick=WordClick('"+d[i].myword+"')>"+d[i].myword+"</a>";
  $("<td/>").html(mywordlink).appendTo($tr);
      $("<td/>").text(d[i].mytype).appendTo($tr);

	  var myset=d[i].myset.split(';');
	  var mydisplay_link="";
	  for (var j in myset)
	  {
	  if (myset[j]!="")
		{
		mydisplay_link+="<a id='action' onClick=WordClick('"+myset[j]+"')>"+myset[j]+"</a>, ";
		}
	  }
	  $("<td/>").html(mydisplay_link).appendTo($tr); 


    }
    $ld.slideUp();
  });
  });
  


});
