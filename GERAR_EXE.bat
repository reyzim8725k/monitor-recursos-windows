@echo off
setlocal
cd /d "%~dp0"
echo ================================================
echo   Gerador do Monitor de Recursos do PC
 echo ================================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python nao foi encontrado.
  echo Instale o Python em https://www.python.org/downloads/windows/
  pause
  exit /b 1
)
py -m pip install --upgrade pyinstaller
if errorlevel 1 (
  echo Falha ao instalar o PyInstaller.
  pause
  exit /b 1
)
py -m PyInstaller --noconfirm --clean --onefile --windowed --name MonitorRecursos monitor_recursos.py
if errorlevel 1 (
  echo Falha ao gerar o EXE.
  pause
  exit /b 1
)
echo.
echo EXE criado em:
echo %CD%\dist\MonitorRecursos.exe
start "" "%CD%\dist"
pause
