#~FILE="adab.txt"
#FILE="rndlines.txt"
FILE="text.txt"
echo "delete cache"
rm -r /tmp/qalsadiCache

echo "test without cache"
DATE=`date +%Y-%m-%d-%H:%M`
LIMIT=500
mkdir -p output/eval/d${DATE}
OUTDIR="output/eval/d${DATE}"

valgrindNoCache="valgrind --tool=massif --time-unit=ms --detailed-freq=20 --massif-out-file=${OUTDIR}/massif.out.nocache"
valgrindCache="valgrind --tool=massif --time-unit=ms --detailed-freq=20 --massif-out-file=${OUTDIR}/massif.out.cache"

${valgrindNoCache} python -m cProfile ../bin/mishkal-console.py -n -p  -l ${LIMIT} -f samples/corpus/${FILE} >output/eval/test.txt
echo "Date; ${DATE} \t ${LIMIT} lines" >> output/eval/file.stats
echo "No Cache" >> output/eval/file.stats
grep "function calls" -2 -h output/eval/test.txt | sed 's/^.*function .* in //g;s/:\*.*$//g' | sed 'N;s/\n//g' >> output/eval/file.stats
echo "make archive" 
mv output/eval/test.txt  ${OUTDIR}/test.nocache
ms_print ${OUTDIR}/massif.out.nocache |grep -v -e "[|-]" |sed -e 's/,//g' > ${OUTDIR}/massif.csv.nocache



echo "test with cache"

${valgrindCache} python -m cProfile ../bin/mishkal-console.py -p  -l ${LIMIT} -f samples/corpus/${FILE} >output/eval/test.txt
echo "With Cache" >> output/eval/file.stats
grep "function calls" -2 -h output/eval/test.txt | sed 's/^.*function .* in //g;s/:\*.*$//g' | sed 'N;s/\n//g' >> output/eval/file.stats
echo "make archive" 
mv output/eval/test.txt  ${OUTDIR}/test.cache
ms_print ${OUTDIR}/massif.out.cache |grep -v -e "[|-]" |sed -e 's/,//g' > ${OUTDIR}/massif.csv.cache


