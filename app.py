# -*- coding: utf-8 -*-
"""
Script to create a streamlist app for users to more easily print QR virus labels
generated in print_labels module

Created on Fri Sep  5 11:02:48 2025

@author: jada.roth
"""

# app.py
import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
import tempfile

# import your existing functions
from print_labels import add_data_to_template

st.title("📦 Virus QR Label Generator")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, dtype=str)
    st.write("✅ File loaded successfully!")
    st.dataframe(df.head())

    if st.button("Generate Labels PDF"):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            # Call your function — this creates one or more PDFs in tmpdir
            add_data_to_template(df, tmpdir_path, x_max=2, y_max=10)

            # Collect generated PDFs (sheets)
            pdf_files = sorted(tmpdir_path.glob("sheet_*.pdf"))
            if not pdf_files:
                st.error("No PDF was generated.")
            elif len(pdf_files) == 1:
                # Single sheet → just offer one download
                pdf_path = pdf_files[0]
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Labels PDF",
                        data=f.read(),
                        file_name=pdf_path.name,
                        mime="application/pdf"
                    )
            else:
                # Multiple sheets → zip them
                import zipfile
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zipf:
                    for pdf_path in pdf_files:
                        zipf.write(pdf_path, pdf_path.name)
                zip_buffer.seek(0)
                st.download_button(
                    label="📥 Download All Label Sheets (ZIP)",
                    data=zip_buffer,
                    file_name="labels.zip",
                    mime="application/zip"
                )
