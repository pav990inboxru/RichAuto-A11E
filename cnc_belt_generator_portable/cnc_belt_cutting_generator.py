import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class CNCGCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("CNC Belt Cutting Code Generator - RichAuto-A11E")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Set up the GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="CNC Belt Cutting Code Generator", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Parameters frame
        params_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
        params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Step parameter
        ttk.Label(params_frame, text="Step (Y-axis increment):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.step_var = tk.DoubleVar(value=40.0)
        self.step_entry = ttk.Entry(params_frame, textvariable=self.step_var, width=15)
        self.step_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Width parameter (X-axis movement)
        ttk.Label(params_frame, text="Width (X-axis length):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.DoubleVar(value=200.0)
        self.width_entry = ttk.Entry(params_frame, textvariable=self.width_var, width=15)
        self.width_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Start Height (Z-axis safe height)
        ttk.Label(params_frame, text="Start Height (Z safe):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.start_height_var = tk.DoubleVar(value=4.0)
        self.start_height_entry = ttk.Entry(params_frame, textvariable=self.start_height_var, width=15)
        self.start_height_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Cut Depth (Z-axis cutting depth)
        ttk.Label(params_frame, text="Cut Depth (Z cut):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cut_depth_var = tk.DoubleVar(value=0.0)
        self.cut_depth_entry = ttk.Entry(params_frame, textvariable=self.cut_depth_var, width=15)
        self.cut_depth_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Plunge Feedrate
        ttk.Label(params_frame, text="Plunge Feedrate:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.plunge_feedrate_var = tk.DoubleVar(value=3000.0)
        self.plunge_feedrate_entry = ttk.Entry(params_frame, textvariable=self.plunge_feedrate_var, width=15)
        self.plunge_feedrate_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Cut Feedrate
        ttk.Label(params_frame, text="Cut Feedrate:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.cut_feedrate_var = tk.DoubleVar(value=300.0)
        self.cut_feedrate_entry = ttk.Entry(params_frame, textvariable=self.cut_feedrate_var, width=15)
        self.cut_feedrate_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Start Y position
        ttk.Label(params_frame, text="Start Y Position:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.start_y_var = tk.DoubleVar(value=0.0)
        self.start_y_entry = ttk.Entry(params_frame, textvariable=self.start_y_var, width=15)
        self.start_y_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # End Y position
        ttk.Label(params_frame, text="End Y Position:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.end_y_var = tk.DoubleVar(value=3320.0)
        self.end_y_entry = ttk.Entry(params_frame, textvariable=self.end_y_var, width=15)
        self.end_y_entry.grid(row=7, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Configure column weights for resizing
        params_frame.columnconfigure(1, weight=1)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=(10, 10))
        
        # Generate button
        self.generate_btn = ttk.Button(buttons_frame, text="Generate Code", command=self.generate_code)
        self.generate_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Save button
        self.save_btn = ttk.Button(buttons_frame, text="Save Code", command=self.save_code)
        self.save_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Save As button
        self.save_as_btn = ttk.Button(buttons_frame, text="Save As...", command=self.save_as_code)
        self.save_as_btn.grid(row=0, column=2)
        
        # Preview text area
        preview_frame = ttk.LabelFrame(main_frame, text="Generated Code Preview", padding="5")
        preview_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Configure main frame grid weights
        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Create text widget with scrollbar
        self.text_area = tk.Text(preview_frame, wrap=tk.NONE, width=70, height=20)
        v_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        h_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL, command=self.text_area.xview)
        
        self.text_area.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Generated code storage
        self.generated_code = ""
        
        # Configure root grid weights
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
    def generate_code(self):
        """Generate CNC code based on the parameters"""
        try:
            step = self.step_var.get()
            width = self.width_var.get()
            start_height = self.start_height_var.get()
            cut_depth = self.cut_depth_var.get()
            plunge_feedrate = self.plunge_feedrate_var.get()
            cut_feedrate = self.cut_feedrate_var.get()
            start_y = self.start_y_var.get()
            end_y = self.end_y_var.get()
            
            # Validate inputs
            if step <= 0:
                messagebox.showerror("Error", "Step must be greater than 0")
                return
            if width <= 0:
                messagebox.showerror("Error", "Width must be greater than 0")
                return
            if start_y > end_y:
                messagebox.showerror("Error", "Start Y must be less than or equal to End Y")
                return
                
            # Generate the code
            code_lines = []
            code_lines.append("G54")
            
            current_y = start_y
            
            # First move to initial position
            code_lines.append(f"G00X0.000Y{current_y:05.0f}Z{start_height:0.3f}")
            
            while current_y <= end_y:
                # Plunge to cut depth
                code_lines.append(f"G01Z{cut_depth:0.3f}F{plunge_feedrate:0.0f}")
                
                # Cut along X-axis
                code_lines.append(f"X{width:0.3f}F{cut_feedrate:0.0f}")
                
                # Retract to safe height
                code_lines.append(f"G00Z{start_height:0.3f}")
                
                # Move to next Y position (but stay at safe height)
                current_y += step
                
                # If we still have more Y positions to cut
                if current_y <= end_y:
                    code_lines.append(f"G00X0.000Y{current_y:05.0f}")
            
            # Add final safe move
            code_lines.append(f"G00Z{start_height:0.3f}")
            
            self.generated_code = "\n".join(code_lines)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, self.generated_code)
            
            self.status_var.set(f"Generated code for {int((end_y-start_y)/step)+1} cuts")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating code: {str(e)}")
            
    def save_code(self):
        """Save the generated code to a file"""
        if not self.generated_code:
            messagebox.showwarning("Warning", "No code generated to save. Please generate code first.")
            return
            
        # Default filename based on parameters
        default_filename = f"belt_cut_{self.width_var.get():.0f}x{self.end_y_var.get():.0f}.nc"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".nc",
            filetypes=[("NC files", "*.nc"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.generated_code)
                self.status_var.set(f"Code saved to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Code successfully saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                
    def save_as_code(self):
        """Save the generated code to a file with custom name"""
        if not self.generated_code:
            messagebox.showwarning("Warning", "No code generated to save. Please generate code first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".nc",
            filetypes=[("NC files", "*.nc"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.generated_code)
                self.status_var.set(f"Code saved to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Code successfully saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def main():
    root = tk.Tk()
    app = CNCGCodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()