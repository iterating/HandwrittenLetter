@echo off
echo Setting up development environment...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or later.
    exit /b 1
)

REM Install Python packages globally if not in virtual env
echo Installing Python packages...
pip install --user flask python-dotenv Pillow flask-cors

REM Install frontend dependencies
echo Installing frontend dependencies...
cd client
call pnpm install

echo Setup complete! Run dev.bat to start the development servers.
pause
