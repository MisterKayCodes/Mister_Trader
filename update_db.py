import sqlite3
import os

db_path = 'mister_trader.db'

def update_schema():
    if not os.path.exists(db_path):
        print(f"Error: Database file {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List of columns to add
    new_columns = [
        ('decision_quality', 'INTEGER'),
        ('emotions', 'TEXT'),
        ('market_condition', 'VARCHAR(50)'),
        ('volatility_level', 'VARCHAR(50)')
    ]
    
    # Get existing columns
    cursor.execute('PRAGMA table_info(trade_psychology)')
    existing_columns = [row[1] for row in cursor.fetchall()]
    
    for col_name, col_type in new_columns:
        if col_name not in existing_columns:
            try:
                print(f"Adding column {col_name}...")
                cursor.execute(f'ALTER TABLE trade_psychology ADD COLUMN {col_name} {col_type}')
                print(f"Successfully added {col_name}")
            except Exception as e:
                print(f"Error adding {col_name}: {e}")
        else:
            print(f"Column {col_name} already exists.")
            
    conn.commit()
    conn.close()
    print("Database sync complete.")

if __name__ == "__main__":
    update_schema()
