import datetime 
import pandas as pd 
from sqlalchemy import create_engine 

print(f"[{datetime.datetime.now()}] 🔬 Mengintip Hasil Akhir di Database...")

# 1. Hubungkan ke file database lokal SQLite
engine = create_engine('sqlite:///northwind.db')

# 2. Kueri untuk mengambil data matang
query = "SELECT * FROM fact_bunker_clean"

try:
    # 3. Tarik datanya ke Pandas
    df_raw = pd.read_sql(query, con=engine)
    print(f"   ✅ [SUKSES] Berhasil menarik {len(df_raw)} baris data dari tabel 'fact_bunker_clean'.\n")
    
    # Supaya terminal VS Code menampilkan semua kolom tanpa terpotong (...)
    pd.set_option('display.max_columns', None)
    
    # 4. Tampilkan 10 baris pertama
    print("--- 10 BARIS DATA PERTAMA ---")
    print(df_raw.head(10))

except Exception as e:
    print("\n❌ Gagal mengintip database. Errornya:")
    print(e)