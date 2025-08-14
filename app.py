import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

class DetectionSystemSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Security Detection System")
        self.root.geometry("400x300")
        
        # Set background color
        self.root.configure(bg='#f0f0f0')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill="both")
        
        # Title Label
        title_label = ttk.Label(
            main_frame, 
            text="Security Detection System",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=20)
        
        # Description Label
        description = ttk.Label(
            main_frame,
            text="Please select the type of detection system:",
            font=('Helvetica', 10)
        )
        description.pack(pady=10)
        
        # Buttons
        style = ttk.Style()
        style.configure('Custom.TButton', padding=10)
        
        intrusion_btn = ttk.Button(
            main_frame,
            text="Intrusion Detection",
            command=self.run_intrusion_detection,
            style='Custom.TButton'
        )
        intrusion_btn.pack(pady=10, padx=50, fill="x")
        
        weapon_btn = ttk.Button(
            main_frame,
            text="Weapon Detection",
            command=self.run_weapon_detection,
            style='Custom.TButton'
        )
        weapon_btn.pack(pady=10, padx=50, fill="x")
        
        # Exit Button
        exit_btn = ttk.Button(
            main_frame,
            text="Exit",
            command=self.root.destroy,
            style='Custom.TButton'
        )
        exit_btn.pack(pady=20, padx=50, fill="x")

    def run_intrusion_detection(self):
        try:
            self.root.withdraw()  # Hide the main window
            os.system('python main.py')
            self.root.deiconify()  # Show the main window again after the script finishes
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Intrusion Detection: {str(e)}")
            self.root.deiconify()

    def run_weapon_detection(self):
        try:
            self.root.withdraw()  # Hide the main window
            os.system('python guiapp.py')
            self.root.deiconify()  # Show the main window again after the script finishes
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Weapon Detection: {str(e)}")
            self.root.deiconify()

def main():
    root = tk.Tk()
    app = DetectionSystemSelector(root)
    root.mainloop()

if __name__ == "__main__":
    main()