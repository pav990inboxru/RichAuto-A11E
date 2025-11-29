import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import os

class CNCCodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("CNC Code Editor - Harper_IDS")
        self.root.geometry("800x600")
        
        # Add title and authorship
        title_label = tk.Label(root, text="CNC Code Editor for RichAuto A11 Controller", font=("Arial", 14, "bold"))
        title_label.pack(pady=5)
        
        author_label = tk.Label(root, text="Developed by Harper_IDS for KД-Group", font=("Arial", 10))
        author_label.pack()
        
        # Manual link for controller documentation
        manual_label = tk.Label(root, text="Controller Manual: https://cnczavod.ru/uploads/docs/kontroller-richauto-dsp-a11e-manual-rus.pdf", 
                               font=("Arial", 9), fg="blue", cursor="hand2")
        manual_label.pack(pady=5)
        manual_label.bind("<Button-1>", lambda e: self.open_manual())
        
        # Create input frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10, fill=tk.X)
        
        # Step input
        tk.Label(input_frame, text="Step (Y):").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.step_entry = tk.Entry(input_frame, width=10)
        self.step_entry.grid(row=0, column=1, padx=5)
        self.step_entry.insert(0, "40")  # Default value
        
        # Width input
        tk.Label(input_frame, text="Width (X):").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.width_entry = tk.Entry(input_frame, width=10)
        self.width_entry.grid(row=0, column=3, padx=5)
        self.width_entry.insert(0, "200")  # Default value
        
        # Height input
        tk.Label(input_frame, text="Height (Y max):").grid(row=0, column=4, padx=5, sticky=tk.W)
        self.height_entry = tk.Entry(input_frame, width=10)
        self.height_entry.grid(row=0, column=5, padx=5)
        self.height_entry.insert(0, "3320")  # Default value
        
        # Length input (not used in current template but available for future use)
        tk.Label(input_frame, text="Length (Z):").grid(row=0, column=6, padx=5, sticky=tk.W)
        self.length_entry = tk.Entry(input_frame, width=10)
        self.length_entry.grid(row=0, column=7, padx=5)
        self.length_entry.insert(0, "4.000")  # Default value
        
        # Speed input
        tk.Label(input_frame, text="Speed (F):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.speed_entry = tk.Entry(input_frame, width=10)
        self.speed_entry.grid(row=1, column=1, padx=5, pady=5)
        self.speed_entry.insert(0, "300")  # Default value
        
        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Load .nc File", command=self.load_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Save", command=self.save_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Save As", command=self.save_as_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Generate Code", command=self.generate_code).pack(side=tk.LEFT, padx=5)
        
        # Text area for code editing
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=30)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Default code template
        self.default_code = """G54
G00X0.000Y000Z4.000
Z4.000
G01Z0.000
X200.000F300
G00Z20.000
X0.000Y40
Z4.000
G01Z0.000
X200.000F300
G00Z20.000
X0.000Y80
Z4.000
G01Z0.000
X200.000F300
G00Z20.000
X0.000Y120
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y160
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y200
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y240
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y280
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y320
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y360
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y400
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y440
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y480
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y520
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y560
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y600
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y640
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y680
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y720
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y760
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y800
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y840
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y880
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y920
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y960
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1000
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1040
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1080
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1120
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1160
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1200
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1240
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1280
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1320
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1360
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1400
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1440
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1480
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1520
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1560
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1600
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1640
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1680
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1720
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1760
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1800
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1840
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1880
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1920
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1960
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2000
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2040
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2080
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2120
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2160
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2200
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2240
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2280
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2320
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2360
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2400
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2440
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2480
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2520
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2560
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2600
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2640
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2680
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2720
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2760
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2800
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2840
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2880
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2920
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2960
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3000
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3040
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3080
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3120
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3160
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3200
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3240
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3280
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3320
Z4.000"""
        
        self.text_area.insert(tk.END, self.default_code)
        
        # Current file path
        self.current_file = None

    def open_manual(self):
        # In a real implementation, this would open the manual link
        messagebox.showinfo("Manual", "Please visit: https://cnczavod.ru/uploads/docs/kontroller-richauto-dsp-a11e-manual-rus.pdf")
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select CNC file",
            filetypes=[("NC files", "*.nc"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.current_file = file_path
                    self.parse_filename_to_inputs(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def parse_filename_to_inputs(self, file_path):
        # Extract step and width from filename like y40x200.nc
        filename = os.path.basename(file_path)
        match = re.match(r'y(\d+)x(\d+)\.nc', filename)
        if match:
            step = match.group(1)
            width = match.group(2)
            self.step_entry.delete(0, tk.END)
            self.step_entry.insert(0, step)
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, width)
    
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                messagebox.showinfo("Success", f"File saved: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        # Generate filename based on step (Y) and width (X) inputs
        step = self.step_entry.get().strip()
        width = self.width_entry.get().strip()
        
        if not step or not width:
            messagebox.showwarning("Warning", "Please enter both Step (Y) and Width (X) values")
            return
        
        # Validate that step and width are numbers
        try:
            float(step)
            float(width)
        except ValueError:
            messagebox.showerror("Error", "Step and Width must be numbers")
            return
        
        default_filename = f"y{step}x{width}.nc"
        
        file_path = filedialog.asksaveasfilename(
            title="Save CNC file",
            defaultextension=".nc",
            initialfile=default_filename,
            filetypes=[("NC files", "*.nc"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                self.current_file = file_path
                messagebox.showinfo("Success", f"File saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def generate_code(self):
        try:
            step = float(self.step_entry.get())
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            length = float(self.length_entry.get())
            speed = int(self.speed_entry.get())
            
            # Validate inputs
            if step <= 0 or width <= 0 or height < 0 or length < 0 or speed <= 0:
                raise ValueError("All values must be positive")
            
            # Generate the CNC code
            code_lines = []
            code_lines.append("G54")
            code_lines.append(f"G00X0.000Y000Z{length:.3f}")
            
            y_pos = 0
            while y_pos <= height:
                # Move to starting position
                code_lines.append(f"Z{length:.3f}")
                code_lines.append("G01Z0.000")
                # Cut line at current Y position
                code_lines.append(f"X{width:.3f}F{speed}")
                # Move up
                code_lines.append(f"G00Z20.000")
                
                y_pos += step
                
                # If there's still more height to cover, move to next Y position
                if y_pos <= height:
                    code_lines.append(f"X0.000Y{y_pos}")
            
            # Set the generated code in the text area
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "\n".join(code_lines))
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}\nPlease enter valid numbers for all fields.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating code: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CNCCodeEditor(root)
    root.mainloop()