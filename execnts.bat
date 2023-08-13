@echo off
setlocal

set SCRIPT_NAME=exec_converted_notebook_to_script.py
set PYTHON_PATH=C:\Python311\python.exe

"%PYTHON_PATH%" "%~dp0%SCRIPT_NAME%" %*

endlocal