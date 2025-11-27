@echo off
echo Starting CNC Belt Cutting Code Generator...
python cnc_belt_cutting_generator.py
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please make sure Python 3.x is installed and added to your PATH
    pause
)