import streamlit as st  # type: ignore
import os
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="Data Sweeper", layout = "wide")

st.markdown(
    """
    <style>
        .sTApp{
            background-color : "black" ;
            color : "white";
            }
        </style>
    """,
    unsafe_allow_html = True
)

st.title("DataSweeper Sterling integrator By Hasnain")
st.write("Transform your files between CSV and Exel formats with built-in data cleaning and visulization Creating project for quarter 1")


uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel): ", type = ["csv", "xlsx"], accept_multiple_files=True)


for file in uploaded_files:
    print(file)
    file_ext = os.path.splitext(file.name)[-1].lower()
    print(file_ext)
    if file_ext == ".csv":
        df = pd.read_csv(file)
    elif file_ext == ".xlsx":
        df = pd.read_excel(file)
    else:
        st.error(f"Unsupported file type: {file.extension}")
        continue


    st.write(f"📄** File Name: ** {file.name}")
    st.write(f"📏** File Size: ** {file.size / 1024:.2f} KB")

    st.write("🔍 Preview of the Uploaded File:")
    st.dataframe(df.head())

    st.subheader("Data cleaing options")

    if st.checkbox(f"Data cleaning for {file.name}"):
        col1, col2 = st.columns(2)

        with col1 :
            if st.button(f"Remove Deplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates Removed!")

        with col2:
            if st.button(f"Fill Missing Value for {file.name}"):
                numeric_cols = df.select_dtypes(include = ["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols]).mean()
                st.write("Missing Values in Numeric Columns Filled with Column Means!")

    st.subheader("🎯 Select Columns to Convert")



