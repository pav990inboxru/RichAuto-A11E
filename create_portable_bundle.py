import os
import shutil
import zipfile
from pathlib import Path

def create_portable_bundle():
    """Create a portable bundle of the CNC generator for USB drive use"""
    
    # Define the bundle directory
    bundle_dir = Path("cnc_belt_generator_portable")
    
    # Create bundle directory if it doesn't exist
    bundle_dir.mkdir(exist_ok=True)
    
    # Files to include in the bundle
    files_to_copy = [
        "cnc_belt_cutting_generator.py",
        "README.md",
        "run_cnc_generator.bat",
        "run_cnc_generator.sh"
    ]
    
    print("Creating portable bundle...")
    
    # Copy files to bundle directory
    for file in files_to_copy:
        if os.path.exists(file):
            print(f"Copying {file}...")
            shutil.copy2(file, bundle_dir / file)
        else:
            print(f"Warning: {file} not found, skipping...")
    
    print(f"\nBundle created in directory: {bundle_dir}")
    print("\nTo use from USB drive:")
    print("1. Copy the entire 'cnc_belt_generator_portable' folder to your USB drive")
    print("2. On Windows: Double-click 'run_cnc_generator.bat' to run the application")
    print("3. On Linux/macOS: Run 'chmod +x run_cnc_generator.sh && ./run_cnc_generator.sh'")
    print("4. Or run directly with: python cnc_belt_cutting_generator.py")
    
    # Optionally create a zip file for easy distribution
    zip_filename = "cnc_belt_generator_portable.zip"
    print(f"\nCreating ZIP archive: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(bundle_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(bundle_dir.parent)
                zipf.write(file_path, arc_path)
    
    print(f"ZIP archive created: {zip_filename}")
    print("\nBundle creation complete!")

if __name__ == "__main__":
    create_portable_bundle()