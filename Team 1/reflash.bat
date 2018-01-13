rem -- download 'sync' from SysInternals -- short link http://goo.gl/32dbAJ

rem -- first time only - copy support files
copy quokka.py D:\
copy boot.py D:\
mkdir D:\drivers
copy drivers\*.py D:\drivers

sync D:\

set /p DUMMY=Hit ENTER to close...
