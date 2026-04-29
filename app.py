import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Judul Aplikasi
st.title("📊 Laporan Dapur Pupis")

# Koneksi ke Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Input Data
with st.form("form_jual"):
    item = st.text_input("Nama Item")
    qty = st.number_input("Jumlah", min_value=1)
    submit = st.form_submit_id("Simpan")
    
    if submit:
        try:
            # Membaca data tanpa embel-embel worksheet untuk tes koneksi utama
            df = conn.read()
            new_data = pd.DataFrame([{"waktu": datetime.now().strftime("%d/%m/%y"), "item": item, "qty": qty}])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(data=updated_df)
            st.success("Data berhasil masuk!")
        except Exception as e:
            st.error(f"Koneksi Gagal: {e}")

# Lihat Data
st.subheader("Data Terakhir")
try:
    st.dataframe(conn.read())
except:
    st.write("Belum ada data.")
