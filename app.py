import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Sistem Laporan Dapur Pupis", layout="wide")

# --- KONEKSI GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- DATA MENU LENGKAP ---
menu_makanan = {
    "Pisang Wijen": 15000, 
    "Hekeng KW": 15000, 
    "Pempek Menul": 15000, 
    "Ayam Pop Sambal Matah": 18000, 
    "Nasi Telor Sambal Matah": 15000, 
    "Mie Ayam Sambal Matah": 18000
}
menu_minuman = {
    "Lemon Tea": 8000, 
    "Matcha Drink": 10000, 
    "Gula Aren Drink": 10000, 
    "Tiramisu Drink": 10000, 
    "Coklat Drink": 10000, 
    "Sunny Milkult": 15000, 
    "Greeny Milkult": 15000
}
menu_topping = {"Tanpa Topping": 0, "Gula Aren": 2000, "Keju": 2000, "Oreo": 2000, "Kacang Almond": 2000, "Coco Chip": 2000}
rasa_pisang = ["Original", "Coklat", "Tiramisu", "Taro", "Stroberi", "Cappucino", "Matcha"]

st.title("📊 Sistem Laporan Dapur Pupis")

tab1, tab2 = st.tabs(["📥 Input Data", "📋 Lihat Database"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛒 Input Penjualan")
        kat = st.radio("Kategori", ["Makanan", "Minuman"], horizontal=True)
        
        if kat == "Makanan":
            item = st.selectbox("Menu Makanan", list(menu_makanan.keys()))
            if item == "Pisang Wijen":
                r = st.selectbox("Pilih Rasa", rasa_pisang)
                t = st.selectbox("Pilih Topping", list(menu_topping.keys()))
                nama_final = f"{item} ({r}) + {t}"
                harga_satuan = menu_makanan[item] + menu_topping[t]
            else:
                nama_final = item
                harga_satuan = menu_makanan[item]
        else:
            item = st.selectbox("Menu Minuman", list(menu_minuman.keys()))
            nama_final = item
            harga_satuan = menu_minuman[item]
            
        qty = st.number_input("Jumlah (Qty)", min_value=1, step=1)
        total_harga = harga_satuan * qty
        st.info(f"Total: Rp {total_harga:,}")

        if st.button("Simpan Penjualan ✅", use_container_width=True):
            try:
                # Menggunakan perintah read paling dasar untuk menghindari Error 400
                existing_data = conn.read(worksheet="penjualan", ttl=0)
                new_data = pd.DataFrame([{
                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "item": nama_final,
                    "qty": qty,
                    "total": total_harga
                }])
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                conn.update(worksheet="penjualan", data=updated_df)
                st.success(f"Berhasil simpan: {nama_final}")
                st.balloons()
            except Exception as e:
                st.error(f"Koneksi Gagal: Pastikan link di Secrets benar dan nama tab adalah 'penjualan'")

    with col2:
        st.subheader("💸 Input Pengeluaran")
        ket = st.text_input("Keterangan Belanja")
        nominal = st.number_input("Nominal Harga (Rp)", min_value=0, step=1000)
        
        if st.button("Simpan Pengeluaran ❌", use_container_width=True):
            try:
                existing_spend = conn.read(worksheet="pengeluaran", ttl=0)
                new_spend = pd.DataFrame([{
                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "keterangan": ket,
                    "total": nominal
                }])
                updated_spend = pd.concat([existing_spend, new_spend], ignore_index=True)
                conn.update(worksheet="pengeluaran", data=updated_spend)
                st.warning(f"Pengeluaran '{ket}' tercatat!")
            except Exception as e:
                st.error(f"Gagal simpan: Pastikan nama tab adalah 'pengeluaran'")

with tab2:
    st.subheader("Data Penjualan Terkini")
    try:
        df_view = conn.read(worksheet="penjualan", ttl=0)
        st.dataframe(df_view, use_container_width=True)
    except:
        st.info("Menghubungkan ke Google Sheets...")
