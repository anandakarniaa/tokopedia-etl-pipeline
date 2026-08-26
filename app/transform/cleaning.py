import pandas as pd


def clean_dataframe(df):

    df = df.copy()

    # Missing Value
    df["Product Name"] = df["Product Name"].fillna("Unknown")
    df["Price"] = df["Price"].fillna("")
    df["Seller"] = df["Seller"].fillna("No Seller")
    df["City"] = df["City"].fillna("Unknown City")
    df["Sold"] = df["Sold"].fillna("0")
    df["Rating"] = df["Rating"].fillna("0")

    # Cleaning Sold
    df["Sold"] = (
        df["Sold"]
        .astype(str)
        .str.lower()
        .str.replace("terjual", "", regex=False)
        .str.replace("+", "", regex=False)
        .str.replace("rb", "000", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )

    # Handle numeric sold values
    def convert_sold(value):
        try:
            if "." in value:
                return int(float(value) * 1000)
            return int(value)
        except (ValueError, TypeError):
            return 0

    df["Sold"] = df["Sold"].apply(convert_sold)

    # Cleaning Price
    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.replace("Rp", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    # Convert data types
    df["Price"] = pd.to_numeric(
        df["Price"],
        errors="coerce"
    )

    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    ).fillna(0).astype(float)

    # Remove duplicate products
    df = df.drop_duplicates(
        subset=["Product Name"],
        keep="first"
    ).reset_index(drop=True)

    return df