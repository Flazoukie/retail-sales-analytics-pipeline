# Retail Sales Analytics Pipeline

An end-to-end AWS data pipeline that transforms raw retail transaction data into curated analytical datasets.  
Built with **AWS S3, Glue, and Athena** using the UCI Online Retail dataset.

## Business Questions

1. **Which products are performing best?**
2. **How do sales vary by month or by country?**
3. **Who are the most valuable customers?**

## High-Level Architecture

Raw → Curated → Analytics  

- **S3 (raw zone)** stores the original CSV  
- **Glue Crawler** detects schema and registers metadata  
- **Glue Job (PySpark)** cleans & transforms data  
- **S3 (curated zone)** stores Parquet output  
- **Athena** queries the curated dataset for insights  

See the `docs/architecture.md` file for the full architecture documentation.

## Repository Structure

docs/ # design docs, diagrams, table specs
glue_jobs/ # PySpark scripts for Glue ETL
sql/ # Athena queries for business questions
data/ # local reference data (excluded from git)
infra/ # optional IaC for the future

## Dataset
UCI Online Retail Dataset (2010–2011)  
https://archive.ics.uci.edu/ml/datasets/Online+Retail

This dataset is provided for educational use only.