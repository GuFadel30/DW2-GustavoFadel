@echo off
echo =====================================
echo Iniciando Biblioteca Escolar...
echo =====================================

:: Ativar ambiente virtual
cd C:\Users\gustavo_fadel\Documents\GitHub
call .\venv\Scripts\activate

:: Abrir backend na porta 8000
cd dw2-gustavo-fadel\backend
start cmd /k "py -m uvicorn app:app --reload"

:: Abrir frontend na porta 5000
cd ..\frontend
start cmd /k "py -m http.server 5000"

echo =====================================
echo Backend rodando em: http://127.0.0.1:8000
echo Frontend rodando em: http://127.0.0.1:5000/index.html
echo =====================================

pause
