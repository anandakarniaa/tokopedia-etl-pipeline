def save_csv(df):

    df.to_csv(
        "data/processed/Data_Seblak_Clean.csv",
        index=False
    )

    print("CSV berhasil disimpan")