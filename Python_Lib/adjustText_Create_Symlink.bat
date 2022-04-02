pushd %~dp0
powershell -Command "New-Item -ItemType HardLink -Path .\adjustText.py -Target ..\..\Python_Lib\adjustText.py"
pause