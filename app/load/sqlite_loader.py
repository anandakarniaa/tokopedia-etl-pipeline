import sqlite3
from pathlib import Path


def save_sqlite(df):

    project_root = Path(__file__).resolve().parents[2]

    database_dir = project_root / "database"
    database_dir.mkdir(parents=True, exist_ok=True)

    database_path = database_dir / "seblak.db"

    conn = sqlite3.connect(database_path)

    try:
        df.to_sql(
            "seblak_products",
            conn,
            if_exists="replace",
            index=False
        )
    finally:
        conn.close()

    print(f"SQLite berhasil disimpan: {database_path}")