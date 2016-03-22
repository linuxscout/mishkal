echo "../bin/mishkal-console.py -c -l 500 -f samples/vocalized/almuhalla.012.txt >output/compare/rndlines.11.txt"
python -m cProfile ../mishkal-console.py -c -l 500 -f samples/vocalized/almuhalla.012.txt >output/compare/rndlines.11.txt
DATE=`date +%Y-%m-%d-%H:%M`
echo "make archive" 
cp output/compare/rndlines.11.txt  output/compare/L${DATE}.txt
echo "save stats"
date >> output/compare/file.stats  
grep "function calls" -1 -h output/compare/rndlines.txt | sed 's/^.*function .* in //g;s/:\*.*$//g' | sed 'N;s/\n//g' >> output/compare/file.stats

