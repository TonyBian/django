@set LogPath=C:\salt\var\log\salt
@set KeepDay=7

net stop salt-minion
ping localhost -n 3 > /nul
copy %LogPath%\minion %LogPath%\minion%date:~0,4%-%date:~5,2%-%date:~8,2%.log
echo '' > %LogPath%\minion 
ping localhost -n 3 > /nul
net start salt-minion

forfiles /p "%LogPath%" /m *.log -d -%KeepDay% /c "cmd /c del /f @path"
