import os
import datetime
import base64

def get_mysql_version(cursor):
    cursor.execute("SELECT VERSION();")
    return cursor.fetchone()[0]

def format_value(val):
    if val is None:
        return "NULL"
    elif isinstance(val, (int, float)):
        return str(val)
    elif hasattr(val, 'isoformat'):
        return f"'{val.isoformat()}'"
    elif isinstance(val, bytes):
        encoded = base64.b64encode(val).decode('ascii')
        return f"'{encoded}'"
    else:
        escaped_val = str(val).replace("'", "''")
        return f"'{escaped_val}'"

def generate_create_query(cursor, db, table):
    cursor.execute(f"SHOW CREATE TABLE {db}.{table}")
    return cursor.fetchone()[1] + ";"

def generate_insert_query(cursor, db, table):
    cursor.execute(f"SELECT * FROM {db}.{table}")
    rows = cursor.fetchall()
    if not rows:
        return "empty set"

    values = []
    for row in rows:
        formatted = [format_value(val) for val in row]
        values.append(f"({', '.join(formatted)})")

    return f"INSERT INTO {table} VALUES\n" + ",\n".join(values) + ";"

def write_backup_file(create_stmt, insert_stmt, db, table, user, version, backup_root):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_folder = os.path.join(backup_root, db)
    os.makedirs(backup_folder, exist_ok=True)

    filename = f"{table}_{timestamp}.txt"
    filepath = os.path.join(backup_folder, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"-- Backup Timestamp: {timestamp}\n")
        f.write(f"-- Database Name: {db}\n")
        f.write(f"-- Table Name: {table}\n")
        f.write(f"-- Backed Up By: {user}\n")
        f.write(f"-- MySQL Version: {version}\n")
        f.write("\n" + ("-"*50) + "\n")
        f.write("QUERY TO CREATE TABLE IN THE DATABASE;\n\n")
        f.write(create_stmt + "\n\n")
        f.write(("-"*50) + "\n")
        f.write("QUERY TO INSERT THE RECORDS INTO THE TABLE;\n\n")
        f.write(insert_stmt + "\n")

def backup_table(cursor, db, table, user, backup_root):
    cursor.execute(f"USE {db}")
    version = get_mysql_version(cursor)
    create_stmt = generate_create_query(cursor, db, table)
    insert_stmt = generate_insert_query(cursor, db, table)
    write_backup_file(create_stmt, insert_stmt, db, table, user, version, backup_root)

def backup_database(cursor, db, user, backup_root):
    cursor.execute(f"USE {db}")
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    for table in tables:
        backup_table(cursor, db, table, user, backup_root)

def backup_all_databases(cursor, user, backup_root):
    cursor.execute("SHOW DATABASES")
    dbs = [d[0] for d in cursor.fetchall() if d[0] not in ['information_schema', 'mysql', 'performance_schema', 'sys']]
    for db in dbs:
        backup_database(cursor, db, user, backup_root)
