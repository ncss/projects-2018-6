rem -- download 'sync' from SysInternals -- short link http://goo.gl/32dbAJ

rem -- first time only - copy support files
rem copy quokka.py D:\
rem copy boot.py D:\
rem mkdir D:\drivers
rem copy drivers\*.py D:\drivers

rem -- update main.py
copy client.py D:\main.py
rem copy improved_display.py D:\improved_display.py
copy client_states.py D:\client_states.py
rem copy pokemon_img.py D:\pokemon_img.py
copy BattleStuff.py D:\BattleStuff.py
copy images.dat D:\images.dat
sync D:\

set /p DUMMY=Hit ENTER to close...
