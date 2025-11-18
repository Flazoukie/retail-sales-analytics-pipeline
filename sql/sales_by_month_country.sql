SELECT 
    country,
    year,
    month,
    SUM(revenue) AS total_sales
FROM retail_curated_db.online_retail_curated
GROUP BY 1, 2, 3
ORDER BY total_sales DESC;
