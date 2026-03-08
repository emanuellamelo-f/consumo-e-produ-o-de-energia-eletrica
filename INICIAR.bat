@echo off
echo Iniciando ENERGYX Dashboard...
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo Abrindo navegador em 6 segundos...
start /B streamlit run app.py
timeout /t 6 /nobreak >nul
start http://localhost:8501
echo.
echo Dashboard aberto no navegador!
echo Mantenha esta janela aberta para o dashboard continuar funcionando.
echo Pressione qualquer tecla para fechar o dashboard...
pause >nul
