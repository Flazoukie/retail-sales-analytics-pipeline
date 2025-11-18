# Architecture Overview

This project implements a simple but scalable AWS analytics pipeline.

## Components

### 1. S3 — Data Lake Storage
- `raw/` zone holds the original `online_retail.csv`
- `curated/` zone contains cleaned Parquet files

### 2. Glue Crawler
- Reads the raw CSV
- Creates the table `online_retail_raw`
- Stores schema in the Glue Data Catalog
- Used only for *raw* data discovery

### 3. Glue ETL Job (PySpark)
Core responsibilities:
- Clean invalid/duplicate rows
- Convert data types
- Handle missing CustomerID
- Derive new fields (`revenue`, `year`, `month`, etc.)
- Write partitioned Parquet to curated zone
- Register curated table in the Data Catalog

### 4. Athena
- Serverless SQL querying engine
- Runs analytical queries on curated data
- Supports dashboards (e.g., QuickSight)

## Data Flow Diagram (to be added)

S3 (raw) → Glue Crawler → Data Catalog  
Data Catalog + Glue Job → S3 (curated) → Athena

## Architecture Diagram

```mermaid
flowchart LR
    subgraph S3["Amazon S3"]
        RAW[(Raw Zone<br/>online_retail.csv)]
        CURATED[(Curated Zone<br/>Parquet files)]
    end

    CRAWLER["AWS Glue Crawler"]
    CATALOG["Glue Data Catalog"]
    JOB["Glue ETL Job (PySpark)"]
    ATHENA["Amazon Athena"]

    RAW --> CRAWLER --> CATALOG
    CATALOG --> JOB
    JOB --> CURATED
    CURATED --> ATHENA

