import os
import mysql.connector as msc


def parse_backup_file(filepath):
    """
    Extracts CREATE and INSERT queries from a formatted backup file.
    Returns: (create_query, insert_query, db_name, table_name)
    """
    filename = os.path.basename(filepath)
    if filename.endswith(".txt") and filename.count("_") >= 2:
        table = filename.split("_")[0]
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        create_idx = lines.index("QUERY TO CREATE TABLE IN THE DATABASE;\n")
        insert_idx = lines.index("QUERY TO INSERT THE RECORDS INTO THE TABLE;\n")

        create_stmt = ''.join(lines[create_idx + 1 : insert_idx - 1]).strip()
        insert_stmt = ''.join(lines[insert_idx + 1 : ]).strip()

        db_name_line = next(line for line in lines if line.startswith("-- Database Name:"))
        db_name = db_name_line.split(":")[1].strip()

        return create_stmt, insert_stmt, db_name, table
    else:
        raise ValueError("Invalid backup file format.")


def parse_backup_folder(folder):
    """
    Parses all backup files in a folder and prints a summary of each.
    """
    if not os.path.isdir(folder):
        print("Invalid backup folder.")
        return

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            try:
                create_stmt, insert_stmt, db_name, table = parse_backup_file(os.path.join(folder, file))
                print(f"Parsed backup for {db_name}.{table}:")
                print(f" - Create Statement: {create_stmt[:50]}...")
                print(f" - Insert Statement: {insert_stmt[:50]}...\n")
            except Exception as e:
                print(f"Failed to parse {file}: {e}")


def recover_from_backups(folder, host, user, password):
    """
    Attempts to recover lost data from backup files in the given folder.
    Ensures that only missing records are restored and redundancy is avoided.
    """
    if not os.path.isdir(folder):
        print("Invalid backup folder.")
        return

    conn = msc.connect(host=host, user=user, password=password)
    cur = conn.cursor()

    for file in sorted(os.listdir(folder)):
        if file.endswith(".txt"):
            try:
                create_stmt, insert_stmt, db_name, table = parse_backup_file(os.path.join(folder, file))
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                cur.execute(f"USE {db_name}")

                # Create table if it doesn't exist
                cur.execute(f"SHOW TABLES LIKE '{table}'")
                if not cur.fetchone():
                    cur.execute(create_stmt)

                # Restore only non-existing records
                temp_table = f"temp_{table}_recovery"
                cur.execute(create_stmt.replace(table, temp_table))
                cur.execute(insert_stmt.replace(table, temp_table))

                col_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' AND TABLE_SCHEMA = '{db_name}'"
                cur.execute(col_query)
                columns = [row[0] for row in cur.fetchall()]
                cols_str = ', '.join(columns)

                dedup_query = f"INSERT INTO {table} ({cols_str})\nSELECT {cols_str} FROM {temp_table} t\nWHERE NOT EXISTS (SELECT 1 FROM {table} o WHERE " + " AND ".join([f"t.{col} = o.{col}" for col in columns]) + ")"

                cur.execute(dedup_query)
                cur.execute(f"DROP TABLE {temp_table}")
                conn.commit()
                print(f"Recovered data for {db_name}.{table} successfully.")

            except Exception as e:
                print(f"Failed to recover from {file}: {e}")

    cur.close()
    conn.close()
