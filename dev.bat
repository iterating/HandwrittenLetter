@echo off
echo Killing any existing node and Python processes...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1

echo Starting development servers...

REM Start frontend
cd client
start cmd /k "pnpm dev"

REM Start backend
cd ..
start cmd /k "python app.py"

echo Development servers started!
echo Frontend: http://localhost:5173
echo Backend: http://localhost:5000
echo Press any key to stop all servers...
pause >nul

REM Kill all node and Python processes
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
