# CNC Belt Cutting Code Generator

This application generates G-code for a belt cutting CNC machine (RichAuto-A11E compatible). It provides a user-friendly interface to adjust cutting parameters and generate the appropriate NC code file.

## Features

- Adjustable parameters for belt cutting operations
- Real-time code preview
- Easy saving of generated code files
- Compatible with RichAuto-A11E control system
- Portable application that runs from USB drive

## Parameters

- **Step**: Y-axis increment between cuts (default: 40.0)
- **Width**: X-axis cutting length (default: 200.0)
- **Start Height**: Z-axis safe height (default: 4.0)
- **Cut Depth**: Z-axis cutting depth (default: 0.0)
- **Plunge Feedrate**: Feedrate for Z-axis plunge (default: 3000)
- **Cut Feedrate**: Feedrate for X-axis cutting (default: 300)
- **Start Y Position**: Starting Y position (default: 0.0)
- **End Y Position**: Ending Y position (default: 3320.0)

## How to Use

1. Run the application: `python cnc_belt_cutting_generator.py`
2. Adjust the parameters according to your cutting requirements
3. Click "Generate Code" to create the G-code
4. Review the generated code in the preview area
5. Click "Save Code" or "Save As..." to save the NC file
6. Transfer the generated .nc file to your CNC machine

## System Requirements

- Python 3.x with tkinter (usually included in standard Python installations)
- Windows, macOS, or Linux operating system

## Portability

This application is designed to run from a USB drive without installation. Simply copy the following files to your USB drive:

- `cnc_belt_cutting_generator.py`
- `README.md` (for instructions)

The application only uses Python standard libraries (including tkinter), so it will run on any system with Python installed.

## Generated Code Format

The application generates G-code compatible with RichAuto-A11E systems in the following format:
- G54 work coordinate system
- Rapid movements (G00) to safe heights and starting positions
- Linear cutting movements (G01) at specified feedrates
- Safe Z-axis retraction between cuts
