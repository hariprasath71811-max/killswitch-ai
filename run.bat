@echo off
REM KillSwitch AI — serve index.html locally (no backend required).
REM The app also runs by double-clicking index.html directly.
python -m http.server 8080
pause
