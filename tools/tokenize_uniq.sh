awk '{
    gsub(/["*^&()#@$,?~]/,"")
    for(i=1;i<=NF;i++){  _[$i]  }
}
END{    for(o in _){ print o }  }' $1
