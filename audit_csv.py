import pandas as pd

df = pd.read_csv("data/processed/Data_Seblak_Clean.csv")

print("Jumlah row:", len(df))

print("\nPrice = 0:")
print((df["Price"] == 0).sum())

print("\nMissing value:")
print(df.isna().sum())

print("\nDuplicate:")
print(df.duplicated().sum())

check = df["Price"] * df["Sold"]

print("\nRevenue salah:")
print((df["Revenue"] != check).sum())