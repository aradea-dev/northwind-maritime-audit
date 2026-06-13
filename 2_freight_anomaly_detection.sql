SELECT 
    o1.order_id,                                          -- 1. ID pengiriman saat ini
    o1.ship_country,                                      -- 2. Negara tujuan
    o1.freight AS biaya_sekarang,                         -- 3. Biaya logistik aktual kapal ini
    (
        SELECT ROUND(AVG(o2.freight), 2)                  -- 4. SUBQUERY: Hitung rata-rata biaya normal khusus untuk negara tersebut
        FROM orders o2 
        WHERE o2.ship_country = o1.ship_country
    ) AS rata_rata_negara,
    CASE 
        -- 5. LOGIKA BISNIS: Jika biaya sekarang > 2.5x rata-rata normal negaranya, tandai sebagai anomali
        WHEN o1.freight > (2.5 * (SELECT AVG(o3.freight) FROM orders o3 WHERE o3.ship_country = o1.ship_country)) 
             THEN '🚩 ANOMALI: Terlalu Mahal'
        ELSE '✅ Normal'
    END AS status_biaya
FROM orders o1
WHERE o1.freight > 150                                    -- 6. Saring hanya untuk pengiriman kargo besar
ORDER BY o1.ship_country ASC, o1.freight DESC;