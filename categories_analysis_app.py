import streamlit as st
import pandas as pd

st.set_page_config(page_title="Category & Item Analysis", layout="wide")

st.title("📊 Category & Item Analysis Tool")

# Upload Excel
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📋 Raw Data Preview")
    st.dataframe(df.head())

    # Store filter
    stores = ["All"] + sorted(df["store"].dropna().unique().tolist())
    selected_store = st.sidebar.selectbox("Select Store", stores)

    # Month filter
    months = ["All"] + sorted(df["month"].dropna().unique().tolist())
    selected_month = st.sidebar.selectbox("Select Month", months)

    filtered_df = df.copy()
    if selected_store != "All":
        filtered_df = filtered_df[filtered_df["store"] == selected_store]
    if selected_month != "All":
        filtered_df = filtered_df[filtered_df["month"] == selected_month]

    st.sidebar.subheader("Choose Analysis")
    analysis_option = st.sidebar.radio(
        "Select Analysis",
        [
            "Top-Selling Categories",
            "Low-Performing Categories",
            "Declining Sub-Categories",
            "Top-Selling Items",
            "Low-Performing Items",
            "ABC Classification",
        ],
    )

    if analysis_option == "Top-Selling Categories":
        top = (
            filtered_df.groupby("Category")["total_amount"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        st.subheader("🔥 Top-Selling Categories")
        st.dataframe(top)

    elif analysis_option == "Low-Performing Categories":
        low = (
            filtered_df.groupby("Category")["total_amount"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )
        st.subheader("🐌 Low-Performing Categories")
        st.dataframe(low)

    elif analysis_option == "Declining Sub-Categories":
        trend = (
            filtered_df.groupby(["month", "SubCategroy"])["total_amount"]
            .sum()
            .reset_index()
        )
        trend["pct_change"] = trend.groupby("SubCategroy")["total_amount"].pct_change()
        declining = trend[trend["pct_change"] < 0]
        st.subheader("📉 Declining Sub-Categories")
        st.dataframe(declining)

    elif analysis_option == "Top-Selling Items":
        top_items = (
            filtered_df.groupby(["Description"])["total_amount"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        st.subheader("⭐ Top-Selling Items")
        st.dataframe(top_items)

    elif analysis_option == "Low-Performing Items":
        low_items = (
            filtered_df.groupby(["Description"])["total_amount"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )
        st.subheader("⚠️ Low-Performing Items")
        st.dataframe(low_items)

    elif analysis_option == "ABC Classification":
        abc = (
            filtered_df.groupby("ItemLookupCode")["total_amount"]
            .sum()
            .reset_index()
            .sort_values("total_amount", ascending=False)
        )
        abc["cumulative_share"] = (
            abc["total_amount"].cumsum() / abc["total_amount"].sum()
        )
        abc["class"] = pd.cut(
            abc["cumulative_share"],
            bins=[0, 0.8, 0.95, 1.0],
            labels=["A", "B", "C"],
            include_lowest=True,
        )
        st.subheader("🔤 ABC Classification")
        st.dataframe(abc)

else:
    st.info("👆 Please upload an Excel file with the expected headers to start.")
