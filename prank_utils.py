import os
import datetime
import random
import string
import backup_utils
from recovery_utils import recover_from_backups

def generate_fake_name(base):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"fake_{base}_{suffix}"

def perform_prank(cursor, db_name, admin_user, backup_root):
    """
    Backs up the database, simulates deletion by renaming tables and DB name.
    """
    print(f"Backing up database '{db_name}' before prank...")
    backup_utils.backup_database(cursor, db_name, admin_user, backup_root)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    prank_db_name = f"DELETED_{timestamp}_{db_name}"

    cursor.execute(f"RENAME DATABASE {db_name} TO {prank_db_name}")
    cursor.execute(f"USE {prank_db_name}")
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        fake_name = generate_fake_name(table)
        cursor.execute(f"RENAME TABLE {prank_db_name}.{table} TO {prank_db_name}.{fake_name}")
        cursor.execute(f"DELETE FROM {fake_name}")
        cursor.execute(f"INSERT INTO {fake_name} VALUES ('You\'ve been pranked!')")

    print(f"Prank complete! Database has been renamed to '{prank_db_name}' and contents hidden.")

def recover_prank(cursor, host, user, password, backup_root):
    """
    Recovers database from prank. Restores original DB name and content.
    """
    print("Scanning for prank databases to recover...")
    cursor.execute("SHOW DATABASES")
    prank_dbs = [db[0] for db in cursor.fetchall() if db[0].startswith("DELETED_")]

    if not prank_dbs:
        print("No prank databases found.")
        return

    for prank_db in prank_dbs:
        original_name = prank_db.split("_", 2)[-1]
        print(f"Recovering '{prank_db}' back to '{original_name}'")
        cursor.execute(f"RENAME DATABASE {prank_db} TO {original_name}")
        recover_from_backups(os.path.join(backup_root, original_name), host, user, password)

    print("Recovery complete.")
