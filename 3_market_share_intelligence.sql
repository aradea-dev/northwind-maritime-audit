-- STEP 1: Buat tabel bayangan pertama bernama 'revenue_komoditas'
WITH revenue_komoditas AS (
    SELECT 
        o.ship_country AS negara_tujuan,                   -- Ambil negara tujuan dari tabel orders
        c.category_name AS nama_komoditas,                 -- Ambil jenis komoditas dari tabel categories
        -- RUMUS REVENUE: Menggunakan unit_price dari tabel products (p) dikali quantity dari order_details (od)
        ROUND(SUM(p.unit_price * od.quantity), 2) AS revenue_per_komoditas
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id   -- Hubungkan order ke detail belanjaan
    INNER JOIN products p ON od.product_id = p.product_id     -- Hubungkan ke tabel produk untuk ambil harga jual
    INNER JOIN categories c ON p.category_id = c.category_id  -- Hubungkan ke kategori komoditasnya
    GROUP BY o.ship_country, c.category_name               -- Kelompokkan hasil per negara dan jenis barang
),

-- STEP 2: Buat tabel bayangan kedua bernama 'total_revenue_negara'
total_revenue_negara AS (
    SELECT 
        negara_tujuan,
        nama_komoditas,
        revenue_per_komoditas,
        -- WINDOW FUNCTION: Hitung TOTAL KESELURUHAN uang di satu negara (mengabaikan jenis barangnya)
        ROUND(SUM(revenue_per_komoditas) OVER(PARTITION BY negara_tujuan), 2) AS total_revenue_seluruh_negara
    FROM revenue_komoditas                                 -- Mengambil data dari hasil STEP 1
)

-- STEP 3: Kueri Utama (Final Output)
SELECT 
    negara_tujuan,
    nama_komoditas,
    revenue_per_komoditas,
    total_revenue_seluruh_negara,
    -- RUMUS PERSENTASE: (Uang Komoditas / Total Uang Negara) * 100 untuk dapat % Kontribusi Pangsa Pasar
    ROUND((revenue_per_komoditas / total_revenue_seluruh_negara) * 100, 2) AS persentase_kontribusi_pasar
FROM total_revenue_negara                                  -- Mengambil data dari hasil STEP 2
WHERE total_revenue_seluruh_negara > 5000                  -- Saring hanya negara besar yang total nilai ekonominya di atas 5.000
ORDER BY negara_tujuan ASC, persentase_kontribusi_pasar DESC; -- Urutkan dari negara A-Z, lalu komoditas dari yang paling dominan