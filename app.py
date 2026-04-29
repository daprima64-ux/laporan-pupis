import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Kedai Laporan Keuangan", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE SEDERHANA ---
if 'penjualan' not in st.session_state:
    st.session_state.penjualan = []
if 'pengeluaran' not in st.session_state:
    st.session_state.pengeluaran = []

# --- DATA MENU ---
menu_makanan = {
    "Pisang Wijen": 15000, "Hekeng KW": 15000, "Pempek Menul": 15000,
    "Ayam Pop Sambal Matah": 18000, "Nasi Telor Sambal Matah": 15000, "Mie Ayam Sambal Matah": 18000
}
menu_minuman = {
    "Lemon Tea": 8000, "Matcha Drink": 10000, "Gula Aren Drink": 10000,
    "Tiramisu Drink": 10000, "Coklat Drink": 10000, "Sunny Milkult": 15000, "Greeny Milkult": 15000
}
menu_topping = {"Tanpa Topping": 0, "Gula Aren": 2000, "Keju": 2000, "Oreo": 2000, "Kacang Almond": 2000, "Coco Chip": 2000}
rasa_pisang = ["Original", "Coklat", "Tiramisu", "Taro", "Stroberi", "Cappucino", "Matcha"]

# --- SIDEBAR: KONTROL KAS ---
st.sidebar.title("💰 Manajemen Kas")
modal_awal = st.sidebar.number_input("Modal Awal Hari Ini", min_value=0, step=1000, value=0)
if st.sidebar.button("⚠️ Reset Data Hari Ini"):
    st.session_state.penjualan = []
    st.session_state.pengeluaran = []
    st.rerun()

# --- HEADER ---
st.title("📊 Sistem Laporan Keuangan Kedai")
st.info(f"Tanggal Operasional: **{datetime.now().strftime('%d %B %Y')}**")

# --- TAB MENU ---
tab_input, tab_laporan, tab_analisis = st.tabs(["📥 Input Data", "📋 Laporan Detail", "📈 Analisis Bisnis"])

with tab_input:
    col_kiri, col_kanan = st.columns(2)
    
    with col_kiri:
        st.subheader("🛒 Catat Penjualan")
        kat = st.radio("Kategori", ["Makanan", "Minuman"], horizontal=True)
        if kat == "Makanan":
            item = st.selectbox("Menu Makanan", list(menu_makanan.keys()))
            if item == "Pisang Wijen":
                r = st.selectbox("Rasa", rasa_pisang)
                t = st.selectbox("Topping", list(menu_topping.keys()))
                nama_f = f"{item} ({r}) + {t}"
                harga_f = menu_makanan[item] + menu_topping[t]
            else:
                nama_f, harga_f = item, menu_makanan[item]
        else:
            item = st.selectbox("Menu Minuman", list(menu_minuman.keys()))
            nama_f, harga_f = item, menu_minuman[item]
        
        qty = st.number_input("Jumlah Porsi", min_value=1, step=1)
        if st.button("Simpan Penjualan ✅", use_container_width=True):
            st.session_state.penjualan.append({"Waktu": datetime.now().strftime("%H:%M"), "Item": nama_f, "Qty": qty, "Total": harga_f * qty})
            st.toast(f"Berhasil mencatat {nama_f}")

    with col_kanan:
        st.subheader("💸 Catat Pengeluaran")
        brg = st.text_input("Nama Barang (Belanja)")
        hrg_b = st.number_input("Total Harga Belanja", min_value=0, step=500)
        if st.button("Simpan Pengeluaran ❌", use_container_width=True):
            if brg:
                st.session_state.pengeluaran.append({"Waktu": datetime.now().strftime("%H:%M"), "Barang": brg, "Total": hrg_b})
                st.toast(f"Pengeluaran {brg} tercatat")

with tab_laporan:
    df_s = pd.DataFrame(st.session_state.penjualan)
    df_p = pd.DataFrame(st.session_state.pengeluaran)
    
    t_masuk = df_s['Total'].sum() if not df_s.empty else 0
    t_keluar = df_p['Total'].sum() if not df_p.empty else 0
    sisa_laci = (modal_awal + t_masuk) - t_keluar

    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Uang Masuk", f"Rp {t_masuk:,}")
    m2.metric("Uang Keluar", f"Rp {t_keluar:,}")
    m3.metric("Sisa Kas (Laci)", f"Rp {sisa_laci:,}")

    st.subheader("Detail Transaksi")
    c_s, c_p = st.columns(2)
    with c_s:
        st.write("**Penjualan**")
        st.dataframe(df_s, use_container_width=True)
    with c_p:
        st.write("**Belanja**")
        st.dataframe(df_p, use_container_width=True)

with tab_analisis:
    if not df_s.empty:
        st.subheader("Menu Paling Laris (Qty)")
        chart_data = df_s.groupby("Item")["Qty"].sum().sort_values(ascending=False)
        st.bar_chart(chart_data)
        
        # Ekspor Data
        csv = df_s.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Laporan Penjualan (CSV)", csv, "laporan_penjualan.csv", "text/csv")
    else:
        st.warning("Belum ada data untuk dianalisis.")