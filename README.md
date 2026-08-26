# Tokopedia ETL Pipeline

A modular and containerized **ETL (Extract, Transform, Load) pipeline** built with Python to collect product data from Tokopedia, transform and validate the dataset, and load the processed data into **PostgreSQL** for further analysis.

The project also integrates **Apache Airflow** for workflow orchestration and **Docker** for containerized execution.

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
             Data Cleaning & Transform
                        │
                        ▼
               Data Validation
                        │
                        ▼
              Feature Engineering
                        │
                        ▼
              ┌─────────┴─────────┐
              ▼                   ▼
          CSV Output         PostgreSQL
                                  │
                                  ▼
                         Exploratory Data
                             Analysis
```

---

## Project Overview

This project implements an end-to-end data pipeline that automates the process of collecting, processing, validating, and storing product data.

The pipeline is designed using a modular architecture where extraction, transformation, validation, and loading processes are separated into dedicated components.

The project demonstrates practical implementation of:

* ETL pipeline development
* Web scraping
* Data cleaning and transformation
* Data validation
* Feature engineering
* PostgreSQL database integration
* Workflow orchestration with Apache Airflow
* Containerization with Docker
* Automated testing
* Exploratory Data Analysis

---

## Features

### 1. Data Extraction

* Scrapes product information from Tokopedia using Selenium.
* Uses BeautifulSoup for HTML parsing.
* Handles dynamically loaded web content.
* Extracts product attributes such as:

  * Product name
  * Price
  * Seller
  * City
  * Sold count
  * Rating

### 2. Data Transformation

* Cleans raw product data.
* Handles missing and inconsistent values.
* Converts columns into appropriate data types.
* Performs feature engineering.
* Creates derived features such as:

  * Revenue
  * Price category
  * Popular product indicator

### 3. Data Validation

The validation process checks the quality of processed data, including:

* Missing values
* Duplicate records
* Data types
* Data consistency
* Required fields

### 4. Data Loading

Processed data can be loaded into:

* CSV
* SQLite
* PostgreSQL

PostgreSQL is used as the primary relational database for the containerized pipeline.

### 5. Workflow Orchestration

Apache Airflow is used to orchestrate the ETL workflow.

The Airflow DAG manages the pipeline stages:

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Load
```

### 6. Containerization

The project uses Docker and Docker Compose to run the pipeline and its supporting services in isolated containers.

Main services include:

* PostgreSQL
* ETL container
* Airflow Database
* Airflow Webserver
* Airflow Scheduler

---

## Project Structure

```text
tokopedia-etl-pipeline/
│
├── airflow/
│   └── dags/
│       └── tokopedia_etl_dag.py
│
├── app/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── extract/
│   │   └── tokopedia_scraper.py
│   │
│   ├── transform/
│   │   ├── cleaning.py
│   │   └── feature_engineering.py
│   │
│   ├── validate/
│   │   └── validator.py
│   │
│   ├── load/
│   │   ├── csv_loader.py
│   │   ├── sqlite_loader.py
│   │   └── postgres.py
│   │
│   └── utils/
│       └── logger.py
│
├── init/
│   └── 01_create_tables.sql
│
├── notebook/
│   └── eda.ipynb
│
├── tests/
│   └── test_postgres.py
│
├── audit_csv.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

---

## Database Schema

The processed product data is stored in a PostgreSQL table named `products`.

Main columns include:

| Column            | Description                  |
| ----------------- | ---------------------------- |
| `id`              | Unique product identifier    |
| `product_name`    | Product name                 |
| `price`           | Product price                |
| `seller`          | Seller name                  |
| `city`            | Seller location              |
| `sold`            | Number of products sold      |
| `rating`          | Product rating               |
| `revenue`         | Estimated revenue            |
| `price_category`  | Product price classification |
| `popular_product` | Popularity indicator         |
| `created_at`      | Record creation timestamp    |

---

## Tech Stack

### Programming & Data Processing

* Python
* Pandas
* NumPy

### Web Scraping

* Selenium
* BeautifulSoup

### Databases

* PostgreSQL
* SQLite

### Workflow Orchestration

* Apache Airflow

### Containerization

* Docker
* Docker Compose

### Testing & Analysis

* Pytest
* Jupyter Notebook
* Exploratory Data Analysis (EDA)

---

## Skills Demonstrated

* ETL Pipeline Development
* Data Engineering
* Web Scraping
* Data Cleaning
* Data Transformation
* Feature Engineering
* Data Validation
* Data Quality Checking
* PostgreSQL Integration
* SQLite Integration
* Workflow Orchestration
* Apache Airflow
* Docker Containerization
* Automated Testing
* Exploratory Data Analysis
* Modular Python Application Design

---

## How to Run

### 1. Clone the repository

```bash
git clone <repository-url>
cd tokopedia-etl-pipeline
```

### 2. Create environment variables

Create a `.env` file in the project root.

Example:

```env
POSTGRES_DB=tokopedia_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

AIRFLOW_DB=airflow
AIRFLOW_USER=airflow
AIRFLOW_PASSWORD=your_airflow_password

AIRFLOW_ADMIN_USER=admin
AIRFLOW_ADMIN_PASSWORD=your_admin_password
AIRFLOW_ADMIN_EMAIL=admin@example.com
```

> Do not commit the `.env` file to GitHub.

### 3. Build and start the containers

```bash
docker compose up -d --build
```

### 4. Check running services

```bash
docker compose ps
```

All required services should be running and healthy.

### 5. Check Airflow

Open:

```text
http://localhost:8080
```

Login using the Airflow credentials configured in `.env`.

### 6. Run the ETL pipeline

The pipeline can be triggered through the Airflow DAG:

```text
tokopedia_etl
```

---

## ETL Pipeline Architecture

```text
                  ┌─────────────────────┐
                  │      Tokopedia      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Selenium +          │
                  │ BeautifulSoup       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Raw Product Data  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Cleaning &          │
                  │ Transformation      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Feature Engineering │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Data Validation     │
                  └──────────┬──────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
          ┌──────────────┐      ┌──────────────┐
          │ CSV Output   │      │ PostgreSQL   │
          └──────────────┘      └───────┬──────┘
                                        │
                                        ▼
                                ┌──────────────┐
                                │     EDA      │
                                └──────────────┘

                  Apache Airflow
                  orchestrates the workflow
```

---

## Data Quality

The pipeline includes validation steps to improve data reliability before loading the data into the database.

Validation includes:

* Missing value detection
* Duplicate detection
* Data type validation
* Required field validation
* Basic data consistency checks

This ensures that invalid or inconsistent records can be identified before entering the final data storage layer.

---

## Testing

The project includes automated tests for the PostgreSQL loading process.

Tests can be executed using:

```bash
pytest
```

---

## Exploratory Data Analysis

The project includes a Jupyter Notebook for exploratory analysis of the processed product data.

The analysis can be used to investigate:

* Product price distribution
* Product popularity
* Seller distribution
* Rating distribution
* Estimated revenue
* Relationship between price and sales

---

## Limitations

Tokopedia uses dynamically loaded content and infinite scrolling. Therefore, the scraper does not represent a complete marketplace crawler.

The number of products retrieved depends on the content available during the scraping session and the configured scrolling behavior.

This project focuses primarily on demonstrating an **end-to-end data engineering workflow**, including extraction, transformation, validation, database loading, orchestration, and containerization, rather than building a large-scale production marketplace crawler.

---

## Future Improvements

Potential improvements include:

* Implement incremental data loading
* Add more robust retry and error handling
* Implement data partitioning
* Add structured logging and monitoring
* Add automated data quality checks
* Improve Airflow task dependency management
* Add CI/CD using GitHub Actions
* Add cloud database integration
* Deploy the pipeline to a cloud environment
* Implement more scalable scraping architecture

---

## Author

Built as a portfolio project to demonstrate practical **Data Engineering, ETL, Python, PostgreSQL, Airflow, and Docker** skills.
