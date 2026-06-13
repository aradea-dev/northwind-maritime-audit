SELECT 
    s.company_name AS nama_kurir,
    COUNT(o.order_id) AS total_shipments,
    ROUND(AVG(o.freight), 2) AS rata_rata_biaya,
    -- Menggunakan JULIANDAY untuk menghitung selisih hari antara tanggal sampai (shipped_date) dan tanggal berangkat (order_date)
    ROUND(AVG(JULIANDAY(o.shipped_date) - JULIANDAY(o.order_date)), 1) AS rata_rata_hari_transit
FROM orders o
INNER JOIN shippers s ON o.ship_via = s.shipper_id
WHERE o.ship_country IN ('France', 'Germany', 'UK', 'Italy', 'Spain') 
  AND o.shipped_date IS NOT NULL
GROUP BY s.company_name
ORDER BY rata_rata_hari_transit DESC;