import pandas as pd


def add_features(df):

    # Estimasi Revenue
    df["Revenue"] = df["Price"] * df["Sold"]

    # Kategori Harga
    df["Price_Category"] = pd.cut(
        df["Price"],
        bins=[0, 10000, 25000, float("inf")],
        labels=["Murah", "Sedang", "Mahal"]
    )

    # Produk Populer
    df["Popular_Product"] = df["Sold"].apply(
        lambda x: "Yes" if x >= 100 else "No"
    )

    return df