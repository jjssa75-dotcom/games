@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
  py -m tactical_rpg.web
  goto :end
)
where python >nul 2>&1
if not errorlevel 1 (
  python -m tactical_rpg.web
  goto :end
)
set "ASTER_RUNTIME=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%ASTER_RUNTIME%" (
  "%ASTER_RUNTIME%" -m tactical_rpg.web
  goto :end
)
echo.
echo Python 3.11 ou superior nao foi encontrado.
echo Instale o Python e execute JOGAR.bat novamente.
pause
:end
