from tkinter import *
from tkinter import messagebox, ttk
import qrcode
from PIL import ImageTk, Image
import os
import csv
from datetime import datetime

# --- SYSTEM CONFIGURATION ---
# We use a dedicated vault for images and a central CSV for the database
SAVE_DIR = "Student_QR_Vault"
CSV_FILE = "Student_Database.csv"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Professional Header Initialization for CSV
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Roll No", "Name", "Branch", "Phone", "Blood Group", "Institution"])

class QrCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Final Year Project: Student QR Management System")
        self.root.geometry("1000x600")
        self.root.config(bg="#f4f7f6")
        self.root.resizable(False, False)

        # State Management (Variables)
        self.var_name = StringVar()
        self.var_roll = StringVar()
        self.var_branch = StringVar()
        self.var_college = StringVar()
        self.var_blood = StringVar()
        self.var_phone = StringVar()

        # --- UI DESIGN ---
        # Blue Header Bar
        self.header = Frame(self.root, bg="#0b3c49", height=80)
        self.header.pack(side=TOP, fill=X)
        
        Label(self.header, text="QrCodeGenerator - Institutional Portal", 
              font=("Helvetica", 22, "bold"), bg="#0b3c49", fg="white").place(x=20, y=20)
        
        # Static Date Display
        curr_date = datetime.now().strftime("%d-%m-%Y")
        Label(self.header, text=f"Session Date: {curr_date}", font=("Arial", 12, "bold"), 
              bg="#0b3c49", fg="#00dfc4").place(x=800, y=30)

        # Form Section (Left)
        self.left_frame = Frame(self.root, bg="white", bd=1, relief="solid")
        self.left_frame.place(x=30, y=100, width=500, height=470)
        
        Label(self.left_frame, text="REGISTRATION FORM", font=("Arial", 14, "bold"), 
              bg="#1e90ff", fg="white").pack(fill=X)

        inner_f = Frame(self.left_frame, bg="white", padx=30, pady=20)
        inner_f.pack(fill=BOTH)

        # Dynamic Form Rows
        rows = [("Student Name*", self.var_name), ("Roll Number*", self.var_roll), 
                ("Branch/Dept", self.var_branch), ("Institution", self.var_college), 
                ("Contact No", self.var_phone)]

        for i, (txt, var) in enumerate(rows):
            Label(inner_f, text=txt, font=("Arial", 11, "bold"), bg="white").grid(row=i, column=0, sticky="w", pady=10)
            Entry(inner_f, textvariable=var, font=("Arial", 11), bg="#f9f9f9", bd=1, relief="solid").grid(row=i, column=1, pady=10, padx=20, sticky="ew")

        # Blood Group (Optional Field)
        Label(inner_f, text="Blood Group", font=("Arial", 11, "bold"), bg="white").grid(row=5, column=0, sticky="w", pady=10)
        self.blood_combo = ttk.Combobox(inner_f, textvariable=self.var_blood, font=("Arial", 10), state="readonly")
        self.blood_combo['values'] = ("A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-")
        self.blood_combo.grid(row=5, column=1, pady=10, padx=20, sticky="w")
        self.blood_combo.set("Select Group")

        # Action Buttons
        btn_frame = Frame(self.left_frame, bg="white")
        btn_frame.pack(side=BOTTOM, pady=30)

        Button(btn_frame, text="GENERATE & LOG", command=self.generate_logic, bg="#0b3c49", fg="white", 
               font=("Arial", 10, "bold"), width=18, height=2, cursor="hand2").pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="RESET FORM", command=self.reset, bg="#dc3545", fg="white", 
               font=("Arial", 10, "bold"), width=12, height=2, cursor="hand2").pack(side=LEFT, padx=10)

        # Preview Section (Right)
        self.right_frame = Frame(self.root, bg="white", bd=1, relief="solid")
        self.right_frame.place(x=560, y=100, width=410, height=470)

        Label(self.right_frame, text="DIGITAL ID PREVIEW", font=("Arial", 14, "bold"), bg="#333", fg="white").pack(fill=X)
        
        self.qr_label = Label(self.right_frame, text="Awaiting Data Input...", font=("Arial", 10), 
                              bg="#f8f9fa", fg="grey", relief="solid", bd=1)
        self.qr_label.place(x=80, y=80, width=250, height=250)

        self.status = Label(self.right_frame, text="System: Ready", font=("Arial", 10), bg="white", fg="#28a745")
        self.status.place(x=0, y=430, relwidth=1)

    # --- CORE PROJECT LOGIC ---
    def generate_logic(self):
        # Validation: Mandatory check for Roll and Name
        if not self.var_name.get().strip() or not self.var_roll.get().strip():
            messagebox.showwarning("Validation Error", "Teacher's Note: Name and Roll Number cannot be empty!")
            return

        # Handling Optional Data
        bg = self.var_blood.get()
        if bg == "Select Group" or not bg:
            bg = "N/A"

        # 1. Formatting Sequential Data for QR Scanner (Top-to-Bottom)
        qr_content = (f"--- STUDENT ID ---\n"
                      f"NAME  : {self.var_name.get().upper()}\n"
                      f"ROLL  : {self.var_roll.get()}\n"
                      f"DEPT  : {self.var_branch.get() or 'N/A'}\n"
                      f"PHONE : {self.var_phone.get() or 'N/A'}\n"
                      f"BLOOD : {bg}\n"
                      f"ORG   : {self.var_college.get() or 'N/A'}\n"
                      f"DATE  : {datetime.now().strftime('%d-%m-%Y')}")

        # 2. QR Generation
        qr_img = qrcode.make(qr_content)
        qr_img = qr_img.resize((240, 240))
        
        # Save PNG Image
        file_path = os.path.join(SAVE_DIR, f"{self.var_roll.get()}.png")
        qr_img.save(file_path)

        # 3. Sequencing Data for CSV Database (Horizontal Alignment)
        # Order: Date, Roll, Name, Branch, Phone, Blood, College
        data_row = [
            datetime.now().strftime("%d-%m-%Y"),
            self.var_roll.get(),
            self.var_name.get(),
            self.var_branch.get() or 'N/A',
            self.var_phone.get() or 'N/A',
            bg,
            self.var_college.get() or 'N/A'
        ]

        try:
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data_row)
        except PermissionError:
            messagebox.showerror("Error", "Please close Student_Database.csv before saving!")
            return

        # 4. Update UI Display
        self.qr_photo = ImageTk.PhotoImage(qr_img)
        self.qr_label.config(image=self.qr_photo, text="", bd=0)
        self.status.config(text=f"SUCCESS: Student {self.var_roll.get()} Registered", fg="#1e90ff")
        messagebox.showinfo("Project Success", "Student Record Logged and QR Generated!")

    def reset(self):
        variables = [self.var_name, self.var_roll, self.var_branch, self.var_college, self.var_phone]
        for v in variables: v.set("")
        self.var_blood.set("Select Group")
        self.qr_label.config(image="", text="Awaiting Data Input...", bd=1)
        self.status.config(text="System: Ready", fg="#28a745")

if __name__ == "__main__":
    root = Tk()
    app = QrCodeGenerator(root)
    root.mainloop()