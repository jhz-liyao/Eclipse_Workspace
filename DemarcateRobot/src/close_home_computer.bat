@echo off
echo.
echo �밴��y�����رձ����Ժ�����̨ת̨����������������رձ�����
choice -c yn -n
if %errorlevel%==1 goto close
if %errorlevel%==2 goto quit
:close
shutdown -m \\192.168.1.102 -s -t 3
shutdown -m \\192.168.1.103 -s -t 3
shutdown -s -t 3
:quit
echo.
echo �˳��ػ�����...
choice  -t 3 -n -d y
:end