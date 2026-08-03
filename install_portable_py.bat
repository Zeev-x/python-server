@echo off
setlocal

set PATH_NAME=reyette_py
set URL_64=https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip
set URL_32=https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-win32.zip

echo Pilih arsitektur (32/64):
set /p ARCH=Enter architecture: 

if "%ARCH%"=="32" (
    set URL=%URL_32%
) else if "%ARCH%"=="64" (
    set URL=%URL_64%
) else (
    echo Invalid input. Harus 32 atau 64.
    pause
    exit /b
)

if not exist "%PATH_NAME%" mkdir "%PATH_NAME%"

echo === Downloading Python embed ===
curl -L -o python.zip %URL% || goto :error

echo === Extracting archive ===
powershell -command "Expand-Archive -Path python.zip -DestinationPath %PATH_NAME%" || goto :error

echo === Downloading get-pip.py ===
curl -L -o "%PATH_NAME%\get-pip.py" https://bootstrap.pypa.io/get-pip.py || goto :error

echo === Installing pip ===
"%PATH_NAME%\python.exe" "%PATH_NAME%\get-pip.py" || goto :error

echo === Writing python312._pth ===
echo python312.zip > "%PATH_NAME%\python312._pth"
echo . >> "%PATH_NAME%\python312._pth"
echo Lib\site-packages >> "%PATH_NAME%\python312._pth"
echo .. >> "%PATH_NAME%\python312._pth"
echo. >> "%PATH_NAME%\python312._pth"
echo # Uncomment to run site.main() automatically >> "%PATH_NAME%\python312._pth"
echo #import site >> "%PATH_NAME%\python312._pth"

echo === Writing pyr.bat ===
echo @echo off > pyr.bat
echo REM %%~dp0 = folder tempat pyr.bat berada >> pyr.bat
echo set PYTHON_PATH=%%~dp0%PATH_NAME%\python.exe >> pyr.bat
echo if exist "%%PYTHON_PATH%%" ( >> pyr.bat
echo     "%%PYTHON_PATH%%" %%* >> pyr.bat
echo ) else ( >> pyr.bat
echo     echo Python portable tidak ditemukan di "%%PYTHON_PATH%%" >> pyr.bat
echo ) >> pyr.bat

del python.zip
del "%PATH_NAME%\get-pip.py"

echo === Installation completed successfully ===
pause
exit /b

:error
echo *** Terjadi error pada langkah sebelumnya ***
pause
exit /b
