import pandas as pd


def clean_dataframe(df):

    # Missing Value
    df["Product Name"] = df["Product Name"].fillna("Unknown")
    df["Price"] = df["Price"].fillna("0")
    df["Seller"] = df["Seller"].fillna("No Seller")
    df["City"] = df["City"].fillna("Unknown City")
    df["Sold"] = df["Sold"].fillna("0")
    df["Rating"] = df["Rating"].fillna("0")

    # Cleaning Sold
    df["Sold"] = (
        df["Sold"]
        .astype(str)
        .str.replace("terjual", "", regex=False)
        .str.replace("+", "", regex=False)
        .str.replace("rb", "", regex=False)
        .str.strip()
    )

    # Cleaning Price
    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.replace("Rp", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.strip()
    )

    # Ubah tipe data
    df["Price"] = df["Price"].astype(int)
    df["Sold"] = df["Sold"].astype(int)
    df["Rating"] = df["Rating"].astype(float)

    # Hapus duplikat
    df = df.drop_duplicates()

    return df