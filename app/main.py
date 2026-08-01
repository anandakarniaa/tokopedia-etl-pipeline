from app.extract.tokopedia_scraper import scrape_tokopedia
from app.transform.cleaning import clean_dataframe
from app.transform.feature_engineering import add_features
from app.validate.validator import validate_dataframe
from app.load.csv_loader import save_csv
from app.load.sqlite_loader import save_sqlite
from app.utils.logger import logger


def main():

    logger.info("===== ETL Pipeline Started =====")

    df = scrape_tokopedia()

    logger.info("Scraping selesai")

    df = clean_dataframe(df)

    logger.info("Cleaning selesai")

    df = add_features(df)

    logger.info("Feature Engineering selesai")

    validate_dataframe(df)

    logger.info("Validation selesai")

    save_csv(df)

    logger.info("CSV berhasil disimpan")

    save_sqlite(df)

    logger.info("SQLite berhasil disimpan")

    logger.info("===== ETL Pipeline Finished =====")


if __name__ == "__main__":
    main()