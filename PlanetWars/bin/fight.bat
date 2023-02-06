@echo off
set i=%3
echo . > game_res.txt
:deb
set /a i=%i+1
if %i% == %4 goto fin
echo Playing map %i%...
echo Map %i% >>game_res.txt
java -jar PlayGame.jar ..\maps\map%i%.txt 2000 200 log.txt "java bot.MasterKnapsackFleetsBot %1 %2" "camlrun bot.exe" > game_out.txt 2>>game_res.txt
Rem echo "Map %i% played."
Rem pause
goto deb
:fin
echo The end