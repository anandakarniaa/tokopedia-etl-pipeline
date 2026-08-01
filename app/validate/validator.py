def validate_dataframe(df):

    if df.empty:
        raise ValueError("Data kosong")

    if (df["Price"] < 0).any():
        raise ValueError("Price tidak boleh negatif")

    if (df["Sold"] < 0).any():
        raise ValueError("Sold tidak boleh negatif")

    if ((df["Rating"] < 0) | (df["Rating"] > 5)).any():
        raise ValueError("Rating harus antara 0-5")

    print("Validation Success")

    return True