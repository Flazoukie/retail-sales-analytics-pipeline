# Data Transformation Rules

These rules define how raw data is cleaned and curated.

## 1. Row Filtering

- Drop rows where `InvoiceNo` is null
- Drop rows where `StockCode` is null
- Drop rows where `Quantity` or `UnitPrice` is null
- Keep negative quantities (represent returns)  
  - Add `is_return = quantity < 0` boolean flag

## 2. Data Type Standardization

- `InvoiceDate` → timestamp
- `Quantity` → integer
- `UnitPrice` → double
- `CustomerID` → string

## 3. Handling Missing CustomerID

Strategy: **retain but mark**  
- Replace null CustomerID with `'UNKNOWN'`

This keeps the dataset complete while still allowing filtering.

## 4. Derived Fields

- `revenue = quantity * unit_price`
- `invoice_date_date = date(invoice_date)`
- `year = year(invoice_date)`
- `month = month(invoice_date)`

## 5. Output Specification

- File format: **Parquet**  
- Compression: **snappy**  
- Partitioning: `year`, `month`  
- Output table name: `online_retail_curated`  
