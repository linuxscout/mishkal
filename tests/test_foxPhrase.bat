rem Copy date and time to the single variable as separated by the single whitespace
rem Skip incorrectness in time earlier than 10:00 - replace of leading whitespaces with '0'
set now=%DATE: =0% %TIME: =0%

rem The %now% variable consists of the string like this "03.10.2009 16:04:58,40"
rem Disassemble date and time on parts
for /f "tokens=1-7 delims=/-:., " %%a in ( "%now%" ) do (
    rem Define your owned delimiters and order of tokens
    set now=%%c%%b%%a_%%d%%e
)
python -m cProfile ..\thalab-console.py -c -f samples/phrases.txt >output/phrases.txt
copy output\phrases.txt output\phrases\%now%.txt
