from pathlib import Path


def save_csv(df):

    project_root = Path(__file__).resolve().parents[2]

    output_dir = project_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "Data_Seblak_Clean.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(f"CSV berhasil disimpan: {output_path}")