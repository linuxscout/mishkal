#python extractUniqWords.py -f samples/vocalized/rndlines.txt >output/uniqwords.tmp.txt
echo " tokenize words,  remove last harakat, "
python extractUniqWords.py -f vo1.txt  >output/uniqwords.tmp.txt
echo "sort and uniq"
sort output/uniqwords.tmp.txt |uniq -c |sort -n -r > output/uniqwords.unq.txt
echo "remove extra whitespace"
sed   "s/^ *//" -i output/uniqwords.unq.txt 
echo " extract uniq vocalized words"
python extractUniqWords.py -r -f output/uniqwords.unq.txt > output/uniqwords.tmp.2.txt
echo "sort extracted words by frequency"
sort -n -r  output/uniqwords.tmp.2.txt > output/uniqwords.txt

