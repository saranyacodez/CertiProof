import tkinter as tk
from tkinter import messagebox
import hashlib
import time
import json
import os

# --- 1. CORE LOGIC (Blockchain) ---
class CertiBlockchain:
    def __init__(self):
        self.chain = []
        self.db_file = "verified_ledger.json"
        # Old data irundha load pannum, illana puthu list create pannum
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as f:
                    self.chain = json.load(f)
            except:
                self.chain = []
        
        if not self.chain:
            # Genesis Block (First block)
            self.chain = [{"index": 0, "hash": "0", "data": "Genesis"}]

    def add_record(self, name, aadhar, cert_no):
        # Name, Aadhaar, Cert Number moonu sethu oru UNIQUE Hash create panrom
        raw_data = f"{aadhar}-{cert_no}-{name}".upper()
        identity_hash = hashlib.sha256(raw_data.encode()).hexdigest()
        
        new_block = {
            "index": len(self.chain),
            "timestamp": time.ctime(),
            "student_name": name.upper(),
            "aadhar_no": aadhar,
            "cert_no": cert_no.upper(),
            "id_hash": identity_hash,
            "prev_hash": self.chain[-1].get("id_hash", "0")
        }
        
        self.chain.append(new_block)
        # JSON file-la save panrom (Ledger)
        with open(self.db_file, "w") as f:
            json.dump(self.chain, f, indent=4)
        return identity_hash

# --- 2. THE UI (Standard Tkinter - No Installation Needed) ---
class App:
    def __init__(self, root):
        self.bc = CertiBlockchain()
        root.title("CertiProof | Secure Blockchain Validator")
        root.geometry("500x600")
        root.configure(bg="#f4f7f6")

        # Header
        tk.Label(root, text="VISION VORTEX: CertiProof", font=("Helvetica", 18, "bold"), bg="#f4f7f6", fg="#2c3e50").pack(pady=20)
        tk.Label(root, text="Aadhaar-Linked Blockchain Ledger", font=("Helvetica", 10), bg="#f4f7f6", fg="#7f8c8d").pack()

        # Input Fields
        self.create_label_entry(root, "STUDENT NAME", "name")
        self.create_label_entry(root, "AADHAAR NUMBER", "aadhar")
        self.create_label_entry(root, "CERTIFICATE NUMBER", "cert")

        # Action Buttons
        tk.Button(root, text="Register on Blockchain", command=self.register, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"), width=25, height=2, bd=0).pack(pady=15)
        tk.Button(root, text="Verify Authenticity", command=self.verify, bg="#2ecc71", fg="white", font=("Helvetica", 12, "bold"), width=25, height=2, bd=0).pack(pady=5)

        # Status Display
        self.status_box = tk.Frame(root, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        self.status_box.pack(pady=30, padx=40, fill="x")
        
        self.status = tk.Label(self.status_box, text="SYSTEM READY", font=("Helvetica", 12, "bold"), bg="white", fg="#2f3640")
        self.status.pack(pady=15)

    def create_label_entry(self, root, txt, var_name):
        tk.Label(root, text=txt, bg="#f4f7f6", font=("Helvetica", 9, "bold"), fg="#34495e").pack(pady=(10, 0))
        entry = tk.Entry(root, font=("Helvetica", 12), width=35, justify='center', bd=1, relief="solid")
        entry.pack(pady=5, ipady=5)
        setattr(self, var_name, entry)

    def register(self):
        n, a, c = self.name.get().strip(), self.aadhar.get().strip(), self.cert.get().strip()
        if not n or not a or not c:
            messagebox.showwarning("Input Error", "Please fill all fields for Registration")
            return
        
        h = self.bc.add_record(n, a, c)
        self.status.config(text="✅ REGISTERED SUCCESSFULLY", fg="#27ae60")
        messagebox.showinfo("Blockchain Update", f"Data Hashed & Added to Ledger!\n\nHash ID: {h[:24]}...")

    def verify(self):
        n, a, c = self.name.get().strip(), self.aadhar.get().strip(), self.cert.get().strip()
        
        # Step 1: Input details-ah vachu oru hash create panrom
        input_raw = f"{a}-{c}-{n}".upper()
        input_hash = hashlib.sha256(input_raw.encode()).hexdigest()
        
        # Step 2: Ledger-la check panrom
        found = False
        for block in self.bc.chain:
            # Check if this certificate number exists in any block
            if block.get("cert_no") == c.upper():
                # If cert matches, check if the Aadhaar+Name hash also matches
                if block.get("id_hash") == input_hash:
                    found = True
                    break
        
        if found:
            self.status.config(text="✅ AUTHENTIC RECORD FOUND", fg="#27ae60")
            messagebox.showinfo("Result", "Success! This certificate is verified against the Aadhaar Blockchain.")
        else:
            self.status.config(text="❌ FAKE / IDENTITY MISMATCH", fg="#e74c3c")
            messagebox.showerror("Result", "Verification Failed! The Aadhaar number or Name does not match the record for this Certificate.")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()