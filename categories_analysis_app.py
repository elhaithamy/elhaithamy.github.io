import streamlit as st
import pandas as pd

st.set_page_config(page_title="Category & Item Analysis", layout="wide")

st.title("📊 Category & Item Analysis Tool")

# Upload file
uploaded_file = st.file_uploader("Upload your Excel/CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    # Load based on file type
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    st.success("✅ File uploaded successfully!")
    st.write("### Preview of Data")
    st.dataframe(df.head())

    # Sidebar filters
    stores = ["All"] + df["store"].dropna().unique().tolist()
    store_filter = st.sidebar.selectbox("Select Store", stores)

    months = ["All"] + df["month"].dropna().unique().tolist()
    month_filter = st.sidebar.selectbox("Select Month", months)

    # Apply filters
    df_filtered = df.copy()
    if store_filter != "All":
        df_filtered = df_filtered[df_filtered["store"] == store_filter]
    if month_filter != "All":
        df_filtered = df_filtered[df_filtered["month"] == month_filter]

    # Select analysis
    analysis_type = st.radio("Choose analysis:", [
        "Top-Selling Categories",
        "Low-Performing Categories",
        "Declining Sub-Categories",
        "Item-Level Performance"
    ])

    if analysis_type == "Top-Selling Categories":
        result = df_filtered.groupby("Category")["total_amount"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(result)

    elif analysis_type == "Low-Performing Categories":
        result = df_filtered.groupby("Category")["total_amount"].sum().sort_values().head(10)
        st.bar_chart(result)

    elif analysis_type == "Declining Sub-Categories":
        trend = df_filtered.groupby(["month", "SubCategroy"])["total_amount"].sum().reset_index()
        st.line_chart(trend, x="month", y="total_amount", color="SubCategroy")

    elif analysis_type == "Item-Level Performance":
        result = df_filtered.groupby("Description")[["n_order", "total_amount"]].sum().sort_values("total_amount", ascending=False).head(20)
        st.dataframe(result)

else:
    st.info("👆 Please upload a file to get started.")
