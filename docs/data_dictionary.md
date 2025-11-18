# Data Dictionary — Curated Table

This table describes the schema of the curated dataset stored in the curated S3 zone.

| Column              | Type      | Description |
|---------------------|-----------|-------------|
| invoice_no          | string    | Unique invoice/transaction ID |
| invoice_date        | timestamp | Timestamp of purchase |
| invoice_date_date   | date      | Date-only version of invoice_date |
| stock_code          | string    | Product identifier |
| description         | string    | Product description |
| quantity            | int       | Units purchased (negative = return) |
| unit_price          | double    | Price per unit |
| revenue             | double    | quantity × unit_price |
| customer_id         | string    | Customer ID or 'UNKNOWN' |
| country             | string    | Customer country |
| year                | int       | Year of transaction |
| month               | int       | Month of transaction |
| is_return           | boolean   | True if quantity < 0 |

Partitioned by (`year`, `month`) and stored as **Parquet**.
