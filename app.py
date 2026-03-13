# -*- coding: utf-8 -*-
"""
Script to create a streamlit app for users to more easily print QR virus labels
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
from print_labels import add_data_to_template, load_file
 
st.title("📦 Virus QR Label Generator")

st.markdown("""
            Please upload a csv, tsv, or excel file with the following column names:
            
                VT
               
                Plasmid
                
                Name
                
                Serotype
               
                FullName
               
                
            If needed, please download a label template below!
            Please contact Jada (jada.roth@alleninstitute.org) with questions🐱 
            """)
            
template_df = pd.DataFrame(columns=["VT", "Plasmid", "Name", "Serotype", "FullName"])
csv_bytes = template_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download CSV Template",
    data=csv_bytes,
    file_name="label_template.csv",
    mime="text/csv"
)
            
uploaded_file = st.file_uploader(
    "Upload your data file",
    type=["csv", "tsv", "xlsx", "xls", "ods"]
)
 
if uploaded_file is not None:
    # Write upload to a temp file so load_file can detect the extension
    suffix = Path(uploaded_file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = Path(tmp.name)
 
    try:
        df = load_file(tmp_path)
        st.write("✅ File loaded successfully!")
        st.dataframe(df.head())
    except ValueError as e:
        st.error(f"❌ Could not read file: {e}")
        st.stop()
    finally:
        tmp_path.unlink(missing_ok=True)  # clean up temp file
 
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
