from app.extract.tokopedia_scraper import scrape_tokopedia
from app.transform.cleaning import clean_dataframe
from app.transform.feature_engineering import add_features
from app.validate.validator import validate_dataframe
from app.load.csv_loader import save_csv
from app.load.sqlite_loader import save_sqlite
from app.load.postgres import save_postgres
from app.utils.logger import logger


def main():

    logger.info("===== ETL Pipeline Started =====")

    df = scrape_tokopedia()

    logger.info("Scraping selesai")

    # print(f"DEBUG setelah scraping: {len(df)}")

    df = clean_dataframe(df)

    logger.info("Cleaning selesai")

    # print(f"DEBUG setelah cleaning: {len(df)}")

    df = add_features(df)

    logger.info("Feature Engineering selesai")

    # print(f"DEBUG setelah feature engineering: {len(df)}")

    validate_dataframe(df)

    logger.info("Validation selesai")

    # print(f"DEBUG setelah validation: {len(df)}")

    save_csv(df)

    logger.info("CSV berhasil disimpan")

    save_sqlite(df)

    logger.info("SQLite berhasil disimpan")

    # print(f"DEBUG sebelum PostgreSQL: {len(df)}")

    save_postgres(df)

    logger.info("PostgreSQL berhasil disimpan")

    logger.info("===== ETL Pipeline Finished =====")


if __name__ == "__main__":
    main()