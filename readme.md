Hotmail IMAP Account Checker

Description

This script automates checking the login status of Hotmail/Outlook accounts using the IMAP protocol. It provides a simple graphical interface (GUI) to upload a file containing email-password pairs and processes them sequentially. Successful logins are saved in valid_accounts.txt, and failed logins are stored in failed_accounts.txt.

Features

GUI-Based File Upload: Easily select an account list file.

Progress Tracking: Displays real-time login attempts.

Multithreading: Runs checks without freezing the interface.

Error Handling: Separates valid and failed accounts into respective files.

Notification on Completion: Alerts the user when processing is done.

Requirements

Ensure you have Python 3 installed along with the necessary dependencies:

sudo apt update && sudo apt install python3-tk -y 

Installation & Usage

Clone the repository: git clone https://github.com/your-repo/hotmail-imap-checker.git cd hotmail-imap-checker 

Run the script: python3 hotmail_imap_checker.py 

Select your accounts file (formatted as email:password per line).

View the results in: 

valid_accounts.txt (successful logins)

failed_accounts.txt (failed logins)

Example Input Format

email1@hotmail.com:password1 email2@hotmail.com:password2 email3@hotmail.com:password3 

Notes

The script supports Hotmail and Outlook accounts using IMAP.

Ensure your file is formatted correctly before running the script.

If the GUI does not appear on Linux, try running with python3 -m tkinter to check if Tkinter is installed.

License

This project is for personal use only. Unauthorized use for credential checking beyond owned accounts is strictly prohibited.

