### 🎭 MySQL Prank Tool — Harkat++

A harmless and reversible prank utility that simulates the deletion of a MySQL database. It secretly renames the database and its tables while preserving all original data in a backup — and lets you restore everything later.

---

## 🔥 Features

- 🎯 Simulates database deletion without actually removing anything.
- 🛡️ Backs up the full database before the prank using SQL scripts.
- 😱 Renames the database and tables to give the illusion of deletion.
- ✨ Inserts funny fake data like `"You've been pranked!"`
- ♻️ Easily recover everything from backups without any redundancy.
- 🧱 Modular design with safe SQL practices.

---

## 🧩 Project Structure

```
prank_tool/
├── main.py              # Entry point (menu-driven)
├── prank_utils.py       # Prank logic and recovery
├── recovery_utils.py    # For parsing and restoring backup data
├── backup_utils.py      # Provides functions for recovery file
└── backups/             # Stores .txt backup files
```

---

## 🚀 How to Run

# 1. Install Requirements

```bash
pip install -r requirements.txt
```

# 2. Configure Inputs

Open `main.py` and set your MySQL credentials and target DB name:

```python
host = ""
user = ""
password = ""
db_name = ""
admin_user = ""
backup_root = ""
```

# 3. Run the Script

```bash
python main.py
```

You'll see:
```
Select an operation:
1. Perform Database Prank
2. Recover from Prank
```

---

## 📦 Backup File Format

Backups are stored in `.txt` format with full metadata:
```
-- Backup Timestamp: YYYY-MM-DD HH:MM:SS
-- Database Name: your_db
-- Table Name: your_table
-- Backed Up By: admin_user
-- MySQL Version: 8.x

--------------------------------------------------
QUERY TO CREATE TABLE IN THE DATABASE;

CREATE TABLE your_table (...);

--------------------------------------------------
QUERY TO INSERT THE RECORDS INTO THE TABLE;

INSERT INTO your_table VALUES (...);
```

---

## ♻️ Recovery Mode

- Renames prank database back to its original name.
- Uses `.txt` backups to restore missing data without duplication.
- Automatically re-creates tables and inserts only non-existing records.

---

## 🔐 Safety Notes

- **Does NOT actually delete** any real data or drop databases.
- Can safely prank yourself or friends running test databases.

---

## 👨‍💻 Author

**Yug Agarwal**
- 📧 [yugagarwal704@gmail.com](mailto:yugagarwal704@gmail.com)
- 🔗 GitHub – [@HelloYug](https://github.com/HelloYug)