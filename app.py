import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Laporan Dapur Pupis", layout="wide")

# Inisialisasi koneksi
conn = st.connection("gsheets", type=GSheetsConnection)

# Data Menu
menu_makanan = {"Pisang Wijen": 15000, "Hekeng KW": 15000, "Pempek Menul": 15000, "Ayam Pop Sambal Matah": 18000, "Nasi Telor Sambal Matah": 15000, "Mie Ayam Sambal Matah": 18000}
menu_minuman = {"Lemon Tea": 8000, "Matcha Drink": 10000, "Gula Aren Drink": 10000, "Tiramisu Drink": 10000, "Coklat Drink": 10000, "Sunny Milkult": 15000, "Greeny Milkult": 15000}

st.title("📊 Sistem Laporan Dapur Pupis")

tab_input, tab_laporan = st.tabs(["📥 Input", "📋 Database"])

with tab_input:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛒 Jual")
        item = st.selectbox("Menu", list(menu_makanan.keys()) + list(menu_minuman.keys()))
        qty = st.number_input("Qty", min_value=1)
        if st.button("Simpan Penjualan"):
            try:
                # Membaca data tanpa argumen tambahan untuk menghindari Error 400
                df = conn.read(worksheet="penjualan")
                new_row = pd.DataFrame([{"waktu": datetime.now().strftime("%Y-%m-%d %H:%M"), "item": item, "qty": qty, "total": 0}])
                updated = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="penjualan", data=updated)
                st.success("Tersimpan!")
            except Exception as e:
                st.error(f"Error: {e}")

with tab_laporan:
    try:
        st.dataframe(conn.read(worksheet="penjualan"), use_container_width=True)
    except:
        st.info("Koneksi sedang dimuat...")
