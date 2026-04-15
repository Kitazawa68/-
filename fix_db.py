import pymysql
import configparser
import os

def get_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)
    return config

# Read connection info from config.ini
config = get_config()
conn = pymysql.connect(
    host=config.get('mysql', 'host'),
    port=config.getint('mysql', 'port'),
    user=config.get('mysql', 'user'),
    password=config.get('mysql', 'password'),
    charset='utf8mb4'
)
cursor = conn.cursor()

def run_sql_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Simple split by ;, doesn't work for stored procedures
    if 'generate_10k.sql' in filepath:
        cursor.execute("DROP PROCEDURE IF EXISTS SeedMassiveData;")
        proc_body_start = sql.find("CREATE PROCEDURE")
        proc_body_end = sql.find("END$$") + 3
        proc_body = sql[proc_body_start:proc_body_end]
        cursor.execute(proc_body)
        cursor.execute("CALL SeedMassiveData();")
    else:
        # Split normal SQL statements
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        for stmt in statements:
            if stmt:
                cursor.execute(stmt)
                
    conn.commit()
    print(f"Executed: {filepath}")

# SQL files are at the root level
base_dir = os.path.dirname(__file__)

# 1. Init schema
run_sql_file(os.path.join(base_dir, 'campus_trade_init.sql'))

# 2. Mock data
run_sql_file(os.path.join(base_dir, 'campus_trade_mock_data.sql'))

# 3. 10k data
run_sql_file(os.path.join(base_dir, 'generate_10k.sql'))

conn.close()

# 4. Run db_setup.py to add `dispute` table and modify other tables
import db_setup
db_setup.setup_db()

print("All done!")
