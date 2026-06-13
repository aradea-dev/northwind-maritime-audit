import datetime # import library datetime
import pandas as pd #import library panda
from sqlalchemy import create_engine #import sqlalchemy

def run_maritime_etl():
    print(f"[{datetime.datetime.now()}] 🚀 SOP-1: Menginisiasi Kpler Bunker Tracking ETL Pipeline...")
    
    # 1. EXTRACT: Hubungkan ke database menggunakan SQLAlchemy Engine
    engine = create_engine('sqlite:///northwind.db')
    
    # Kueri PascalCase (Skema Asli SQLite Northwind)
    query = """
    SELECT 
        o.OrderID AS order_id, 
        s.CompanyName AS nama_kurir,
        o.ShipCountry AS negara_tujuan, 
        o.Freight AS biaya_freight, 
        o.ShippedDate AS shipped_date, 
        o.OrderDate AS order_date
    FROM Orders o
    INNER JOIN Shippers s ON o.ShipVia = s.ShipperID
    WHERE o.ShippedDate IS NOT NULL
    """
    df_raw = pd.read_sql(query, con=engine)
    print(f"   ✅ [EXTRACT] Berhasil menarik {len(df_raw)} data transaksi dari database.")

    # 2. TRANSFORM: Investigasi Kualitas Data & Rekonsiliasi (Pandas)
    print("   🔍 [TRANSFORM] Memulai Investigasi Kualitas Data...")
    
    # Menggunakan format='mixed' untuk mengurai stempel waktu secara adaptif
    df_raw['shipped_date'] = pd.to_datetime(df_raw['shipped_date'], format='mixed')
    df_raw['order_date'] = pd.to_datetime(df_raw['order_date'], format='mixed')
    
    # Hitung waktu transit aktual di laut (Backtesting metric)
    df_raw['hari_transit'] = (df_raw['shipped_date'] - df_raw['order_date']).dt.days

    
    # SOP Kpler: Tangani anomali data (jika ada tanggal terbalik)
    data_error = df_raw[df_raw['hari_transit'] < 0]
    
    if not data_error.empty:
        print(f"   🚩 WARNING: Ditemukan {len(data_error)} baris data tanggal terbalik. Otomatis dibersihkan.")
        df_raw = df_raw[df_raw['hari_transit'] >= 0]

    # Deteksi Anomali Biaya: Tandai jika biaya > 2.5x dari rata-rata negara tersebut
    rerata_negara = df_raw.groupby('negara_tujuan')['biaya_freight'].transform('median')
    df_raw['is_cost_anomaly'] = (df_raw['biaya_freight'] > (2.5 * rerata_negara)).astype(int)
    
    df_clean = df_raw.copy()
    print("   ✅ [TRANSFORM] Pembersihan data dan penghitungan metrik selesai.")

    # 3. LOAD: Ekspor ke CSV & Simpan ke Data Mart
    print("   💾 [LOAD] Menyimpan data hasil pemrosesan...")
    
    csv_filename = 'bunker_analysis_ready.csv'
    df_clean.to_csv(csv_filename, index=False)
    print(f"   ✅ [LOAD] Berhasil mengekspor file: '{csv_filename}'")
    
    df_clean.to_sql('fact_bunker_clean', con=engine, if_exists='replace', index=False)
    print(f"   🎉 [{datetime.datetime.now()}] Pipeline sukses berjalan 100%!")

if __name__ == "__main__":
    run_maritime_etl()