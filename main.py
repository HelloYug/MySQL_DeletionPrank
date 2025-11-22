from prank_utils import perform_prank, recover_prank
import mysql.connector as msc
import os

# ----------------------------
# INPUTS (Set your values here)
# ----------------------------
host = ""
user = ""
password = ""
db_name = ""
admin_user = ""
backup_root = ""

# ----------------------------
# MENU
# ----------------------------
print("Select an operation:")
print("1. Perform Database Prank")
print("2. Recover from Prank")

choice = input("Enter choice (1/2): ").strip()

if choice not in ["1", "2"]:
    print("Invalid choice. Exiting.")
    exit()

# Establish connection
mydb = msc.connect(host=host, user=user, password=password)
mycur = mydb.cursor()

if choice == "1":
    perform_prank(mycur, db_name, admin_user, backup_root)

elif choice == "2":
    recover_prank(mycur, host, user, password, backup_root)

mydb.close()
