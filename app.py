import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Laporan Dapur Pupis", layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)

# Data Menu
menu_makanan = {"Pisang Wijen": 15000, "Hekeng KW": 15000, "Pempek Menul": 15000, "Ayam Pop Sambal Matah": 18000, "Nasi Telor Sambal Matah": 15000, "Mie Ayam Sambal Matah": 18000}
menu_minuman = {"Lemon Tea": 8000, "Matcha Drink": 10000, "Gula Aren Drink": 10000, "Tiramisu Drink": 10000, "Coklat Drink": 10000, "Sunny Milkult": 15000, "Greeny Milkult": 15000}
menu_topping = {"Tanpa Topping": 0, "Gula Aren": 2000, "Keju": 2000, "Oreo": 2000, "Kacang Almond": 2000, "Coco Chip": 2000}
rasa_pisang = ["Original", "Coklat", "Tiramisu", "Taro", "Stroberi", "Cappucino", "Matcha"]

st.title("📊 Sistem Laporan Dapur Pupis")

t1, t2 = st.tabs(["📥 Input", "📋 Database"])

with t1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🛒 Jual")
        kat = st.radio("Kategori", ["Makanan", "Minuman"], horizontal=True)
        item = st.selectbox("Menu", list(menu_makanan.keys()) if kat == "Makanan" else list(menu_minuman.keys()))
        if kat == "Makanan" and item == "Pisang Wijen":
            r, t = st.selectbox("Rasa", rasa_pisang), st.selectbox("Topping", list(menu_topping.keys()))
            nama_f, hrg_f = f"{item} ({r}) + {t}", menu_makanan[item] + menu_topping[t]
        else:
            nama_f, hrg_f = item, menu_makanan[item] if kat == "Makanan" else menu_minuman[item]
        
        qty = st.number_input("Qty", min_value=1)
        if st.button("Simpan Penjualan"):
            try:
                # PERBAIKAN: Menggunakan argumen 'sheet' sebagai pengganti 'worksheet'
                df = conn.read(sheet="penjualan", ttl=0)
                new_row = pd.DataFrame([{"waktu": datetime.now().strftime("%Y-%m-%d %H:%M"), "item": nama_f, "qty": qty, "total": hrg_f * qty}])
                updated = pd.concat([df, new_row], ignore_index=True)
                conn.update(sheet="penjualan", data=updated)
                st.success("Berhasil Tersimpan!")
            except Exception as e:
                st.error(f"Gagal: {e}")

    with c2:
        st.subheader("💸 Belanja")
        ket = st.text_input("Keterangan")
        hrg = st.number_input("Harga", min_value=0)
        if st.button("Simpan Pengeluaran"):
            try:
                df_b = conn.read(sheet="pengeluaran", ttl=0)
                new_row_b = pd.DataFrame([{"waktu": datetime.now().strftime("%Y-%m-%d %H:%M"), "keterangan": ket, "total": hrg}])
                updated_b = pd.concat([df_b, new_row_b], ignore_index=True)
                conn.update(sheet="pengeluaran", data=updated_b)
                st.warning("Pengeluaran Tercatat!")
            except Exception as e:
                st.error(f"Gagal: {e}")

with t2:
    try:
        data_view = conn.read(sheet="penjualan", ttl=0)
        st.dataframe(data_view, use_container_width=True)
    except:
        st.info("Menunggu data...")
