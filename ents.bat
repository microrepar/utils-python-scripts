@echo off
setlocal

set SCRIPT_NAME=exec_converted_notebook_to_script.py

rem Detectar o interpretador Python virtual ativo
set "PYTHON_EXE="
for /f "tokens=*" %%i in ('where python') do (
    set "PYTHON_EXE=%%i"
    goto :found
)
:found

if not defined PYTHON_EXE (
    echo Interpretador Python não encontrado. Certifique-se de que um ambiente virtual está ativado.
    exit /b 1
)

"%PYTHON_EXE%" "%~dp0%SCRIPT_NAME%" %*

endlocal
