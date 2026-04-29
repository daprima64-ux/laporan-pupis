import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIG ---
st.set_page_config(page_title="Kedai Laporan Keuangan", layout="wide")

# --- KONEKSI GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- DATA MENU ---
menu_makanan = {"Pisang Wijen": 15000, "Hekeng KW": 15000, "Pempek Menul": 15000, "Ayam Pop Sambal Matah": 18000, "Nasi Telor Sambal Matah": 15000, "Mie Ayam Sambal Matah": 18000}
menu_minuman = {"Lemon Tea": 8000, "Matcha Drink": 10000, "Gula Aren Drink": 10000, "Tiramisu Drink": 10000, "Coklat Drink": 10000, "Sunny Milkult": 15000, "Greeny Milkult": 15000}
menu_topping = {"Tanpa Topping": 0, "Gula Aren": 2000, "Keju": 2000, "Oreo": 2000, "Kacang Almond": 2000, "Coco Chip": 2000}
rasa_pisang = ["Original", "Coklat", "Tiramisu", "Taro", "Stroberi", "Cappucino", "Matcha"]

st.title("📊 Sistem Laporan Kedai (Auto-Save)")

tab_input, tab_laporan = st.tabs(["📥 Input Data", "📋 Lihat Database Sheets"])

with tab_input:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛒 Jual")
        kat = st.radio("Kategori", ["Makanan", "Minuman"], horizontal=True)
        if kat == "Makanan":
            item = st.selectbox("Menu", list(menu_makanan.keys()))
            if item == "Pisang Wijen":
                r, t = st.selectbox("Rasa", rasa_pisang), st.selectbox("Topping", list(menu_topping.keys()))
                nama_f, harga_f = f"{item} ({r}) + {t}", menu_makanan[item] + menu_topping[t]
            else: nama_f, harga_f = item, menu_makanan[item]
        else:
            item = st.selectbox("Menu", list(menu_minuman.keys()))
            nama_f, harga_f = item, menu_minuman[item]
        
        qty = st.number_input("Qty", min_value=1)
        if st.button("Simpan Penjualan ✅", use_container_width=True):
            new_data = pd.DataFrame([{"Waktu": datetime.now().strftime("%Y-%m-%d %H:%M"), "Item": nama_f, "Qty": qty, "Total": harga_f * qty}])
            # AMBIL DATA LAMA DAN GABUNG
            old_data = conn.read(worksheet="Penjualan")
            updated_df = pd.concat([old_data, new_data], ignore_index=True)
            conn.update(worksheet="Penjualan", data=updated_df)
            st.success("Tersimpan di Google Sheets!")

    with col2:
        st.subheader("💸 Belanja")
        brg = st.text_input("Barang")
        hrg_b = st.number_input("Harga", min_value=0)
        if st.button("Simpan Pengeluaran ❌", use_container_width=True):
            new_spend = pd.DataFrame([{"Waktu": datetime.now().strftime("%Y-%m-%d %H:%M"), "Barang": brg, "Total": hrg_b}])
            old_spend = conn.read(worksheet="Pengeluaran")
            updated_spend = pd.concat([old_spend, new_spend], ignore_index=True)
            conn.update(worksheet="Pengeluaran", data=updated_spend)
            st.warning("Pengeluaran tercatat di Sheets!")

with tab_laporan:
    st.write("Data Penjualan Terkini:")
    st.dataframe(conn.read(worksheet="Penjualan"), use_container_width=True)
