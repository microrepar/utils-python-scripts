@echo off
setlocal

set SCRIPT_NAME=notebook_to_scritp.py
set PYTHON_PATH=C:\Python311\python.exe

"%PYTHON_PATH%" "%~dp0%SCRIPT_NAME%" %*

endlocal