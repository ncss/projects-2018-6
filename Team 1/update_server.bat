rem -- download 'sync' from SysInternals -- short link http://goo.gl/32dbAJ

rem -- first time only - copy support files
rem copy quokka.py D:\
rem copy boot.py D:\
rem mkdir D:\drivers
rem copy drivers\*.py D:\drivers

rem -- update main.py
copy server.py D:\main.py
copy BattleStuff.py D:\BattleStuff.py
sync D:\

set /p DUMMY=Hit ENTER to close...
