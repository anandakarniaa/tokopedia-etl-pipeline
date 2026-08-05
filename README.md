# Tokopedia ETL Pipeline

A modular ETL (Extract, Transform, Load) pipeline built with Python to collect product data from Tokopedia, clean and validate the dataset, and store the processed data for further analysis.

---

## ETL Workflow

```text
Tokopedia
    │
    ▼
Selenium + BeautifulSoup
    │
    ▼
Raw Product Data
    │
    ▼
Data Transformation
    │
    ▼
Data Validation
    │
    ▼
CSV Output + SQLite Database
    │
    ▼
Exploratory Data Analysis (EDA)
```

---

## Features

- Extract product information using Selenium and BeautifulSoup
- Clean and transform raw data
- Validate missing values, duplicates, and data types
- Store processed data in CSV and SQLite
- Perform basic Exploratory Data Analysis (EDA) using Jupyter Notebook

---

## Project Structure

```text
tokopedia-etl-pipeline/
│
├── app/
│   ├── config/
│   ├── extract/
│   ├── transform/
│   ├── validate/
│   ├── load/
│   ├── utils/
│   └── main.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── database/
│
├── notebook/
├── requirements.txt
└── README.md
```

---

## Output

```text
data/
├── processed/
│   └── Data_Seblak_Clean.csv
└── database/
    └── tokopedia.db
```

---

## Tech Stack

- Python
- Selenium
- BeautifulSoup
- Pandas
- SQLite
- Jupyter Notebook

---

## Skills Demonstrated

- ETL Pipeline Development
- Web Scraping
- Data Cleaning & Transformation
- Data Validation
- Data Processing with Pandas
- SQLite Database Integration
- Exploratory Data Analysis (EDA)

---

## Limitations

Tokopedia uses infinite scrolling instead of traditional pagination. Therefore, the scraper currently retrieves only the products available on the initially loaded page (approximately 60 products). This project focuses on demonstrating a modular ETL workflow rather than building a large-scale marketplace crawler.

---


```