def validate_dataframe(df):

    if df.empty:
        raise ValueError("Data kosong")

    required_columns = [
        "Product Name",
        "Price",
        "Seller",
        "City",
        "Sold",
        "Rating",
        "Revenue",
        "Price_Category",
        "Popular_Product"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Kolom wajib tidak ditemukan: {missing_columns}"
        )

    if df["Product Name"].isna().any():
        raise ValueError("Product Name mengandung null")

    if df["Price"].isna().any():
        raise ValueError("Price mengandung null")

    if (df["Price"] < 0).any():
        raise ValueError("Price tidak boleh negatif")

    if (df["Sold"] < 0).any():
        raise ValueError("Sold tidak boleh negatif")

    if ((df["Rating"] < 0) | (df["Rating"] > 5)).any():
        raise ValueError("Rating harus antara 0-5")

    if df.duplicated().any():
        raise ValueError("Terdapat duplicate row")

    print("Validation Success")

    return True