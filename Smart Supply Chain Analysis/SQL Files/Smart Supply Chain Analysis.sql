Create database smart_supply_chain;
use smart_supply_chain;
# ----------------------------------------- Business SQL Questions -------------------------------------------------------------
# Which suppliers have the highest shipment volume? 
SELECT s.Supplier_ID,
       s.Supplier_Name,
    COUNT(sh.Shipment_ID) AS Shipment_Volume
FROM cleaned_supplier s
JOIN cleaned_shipment sh
    ON s.Supplier_ID = sh.Supplier_ID
GROUP BY s.Supplier_ID,
		 s.Supplier_Name
ORDER BY Shipment_Volume DESC
Limit 10;

# Which suppliers have the highest average delay? 
SELECT s.Supplier_ID,
       s.Supplier_Name,
    AVG(b.Delay_Hours) AS Average_Delay
FROM cleaned_supplier s
JOIN cleaned_shipment sh
    ON s.Supplier_ID = sh.Supplier_ID
JOIN business_metrics_delay_update b
    ON sh.Shipment_ID = b.Shipment_ID
GROUP BY s.Supplier_ID,
		s.Supplier_Name
ORDER BY Average_Delay DESC;
   
# Which transport mode is used most frequently?   
SELECT Transport_Mode,
    COUNT(*) AS Total_Shipment
FROM cleaned_transportation
GROUP BY Transport_Mode
ORDER BY Total_Shipment DESC;  

# Which transport mode has the lowest average delivery cost?
SELECT t.Transport_Mode,
    ROUND(AVG(b.Delivery_Cost),2) AS Average_Delivery_Cost
FROM cleaned_transportation t
JOIN cleaned_business_metrics b
ON t.Shipment_ID = b.Shipment_ID
GROUP BY t.Transport_Mode
ORDER BY Average_Delivery_Cost ASC;   

# Which warehouses handle the highest shipment volume? 
SELECT w.Warehouse_ID,
       w.Warehouse_City,
    COUNT(sh.Shipment_ID) AS Total_Shipments
FROM cleaned_warehouse w
JOIN cleaned_shipment sh
ON w.Warehouse_ID = sh.Warehouse_ID
GROUP BY w.Warehouse_ID,
         w.Warehouse_City
ORDER BY Total_Shipments DESC;

# How does traffic level affect average delay? 
SELECT e.Traffic_Level,
    ROUND(AVG(b.Delay_Hours), 2) AS Average_Delay
FROM cleaned_external_factors e
JOIN business_metrics_delay_update b
ON e.Shipment_ID = b.Shipment_ID
GROUP BY e.Traffic_Level
ORDER BY Average_Delay DESC;
   
# How does weather condition affect delay?  
SELECT e.Weather_Condition,
    ROUND(AVG(b.Delay_Hours), 2) AS Average_Delay
FROM cleaned_external_factors e
JOIN business_metrics_delay_update b
ON e.Shipment_ID = b.Shipment_ID
GROUP BY e.Weather_Condition
ORDER BY Average_Delay DESC;   

# How does route distance affect average shipment delay?  
SELECT t.Route_Distance,
    ROUND(AVG(b.Delay_Hours), 2) AS Average_Delay
FROM cleaned_transportation t
JOIN business_metrics_delay_update b
ON t.Shipment_ID = b.Shipment_ID
GROUP BY t.Route_Distance
ORDER BY t.Route_Distance;

# Which transport mode handles the highest shipment volume?  
SELECT Transport_Mode,
    COUNT(*) AS Total_Shipments
FROM cleaned_transportation
GROUP BY Transport_Mode
ORDER BY Total_Shipments DESC;

# What are the top suppliers by reliability?
SELECT s.Supplier_Name,
    ROUND(AVG(CASE WHEN b.Delay_Hours = 0 THEN 100 ELSE 0 END), 2) AS Reliability_Score
FROM cleaned_supplier s
JOIN cleaned_shipment sh
ON s.Supplier_ID = sh.Supplier_ID
JOIN business_metrics_delay_update b
ON sh.Shipment_ID = b.Shipment_ID
GROUP BY s.Supplier_Name
ORDER BY Reliability_Score DESC
LIMIT 10;
# --------------------------------------------------------------------------------------------------------------------------
SHOW TABLES;
CREATE TABLE cleaned_business_metrics_backup AS
SELECT *
FROM cleaned_business_metrics;

SELECT COUNT(*) AS Backup_Rows
FROM cleaned_business_metrics_backup;

SELECT COUNT(*)
FROM cleaned_business_metrics;

SELECT COUNT(*) AS Backup_Rows
FROM cleaned_business_metrics_backup;

SELECT COUNT(*) AS Original_Rows
FROM cleaned_business_metrics;

SELECT COUNT(*) AS Staging_Rows,
       COUNT(DISTINCT Shipment_ID) AS Unique_Shipments,
       SUM(CASE WHEN Delay_Hours = 0 THEN 1 ELSE 0 END) AS Zero_Delay
FROM business_metrics_delay_update;
SHOW TABLES;
SET SQL_SAFE_UPDATES = 0;
