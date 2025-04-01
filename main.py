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
    file_extension = os.path.splitext(file.name)[-1].lower()
    
    if file_extension == ".csv":
        df = pd.read_csv(file)
    elif file_extension == ".xlsx":
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
    columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
    df = df[columns]  # Filters the DataFrame to the selected columns
        
        # Visualization section for uploaded data
    st.subheader("📊 Data Visualization")
    if st.checkbox(f"Show Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])  # Plot the first two numeric columns as a bar chart
        
        # Section to choose file conversion type (CSV or Excel)
    st.subheader("🔄 Conversion Options")
    conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()  # Creates in-memory buffer for file output
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)  # Save DataFrame as CSV in buffer
            file_name = file.name.replace(file_extension, ".csv")
            mime_type = "text/csv"
        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False, engine='openpyxl')  # Save as Excel using openpyxl
            file_name = file.name.replace(file_extension, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)
            
            # Download button for the converted file
        st.download_button(
            label=f"⬇️ Download {file.name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
            )

st.success("🎉 All files processed successfully!")



