#!/bin/bash
echo "Starting CNC Belt Cutting Code Generator..."
python3 cnc_belt_cutting_generator.py || python cnc_belt_cutting_generator.py
if [ $? -ne 0 ]; then
    echo "Python is not installed or not in PATH"
    echo "Please make sure Python 3.x is installed"
    read -p "Press any key to continue..."
fi