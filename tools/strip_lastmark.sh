CHARS=$(python -c 'print u"\u064b\u064c\u064d\u064e\u064f\u0651\u0652".encode("utf8")')
sed 's/['"$CHARS"']$//g' < $1
