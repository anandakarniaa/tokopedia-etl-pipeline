import sqlite3


def save_sqlite(df):

    conn = sqlite3.connect("database/seblak.db")

    df.to_sql(
        "seblak_products",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("SQLite berhasil disimpan")