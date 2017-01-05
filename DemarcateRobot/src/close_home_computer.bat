@echo off
echo.
echo 请按“y”键关闭本电脑和另两台转台控制主机，否则请关闭本程序
choice -c yn -n
if %errorlevel%==1 goto close
if %errorlevel%==2 goto quit
:close
shutdown -m \\192.168.1.102 -s -t 3
shutdown -m \\192.168.1.103 -s -t 3
shutdown -s -t 3
:quit
echo.
echo 退出关机程序...
choice  -t 3 -n -d y
:end