import os
import streamlit as st
import pandas as pd
import plotly.express as px
import json


st.set_page_config(page_title="Nationwide Bank Statement App",
                   layout="wide")


def load_transactions(file):
    try:
        df = pd.read_csv(file, encoding='latin-1', skiprows=3)
        df.columns = [col.strip() for col in df.columns]
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")
        df["Paid out"] = df["Paid out"].str.replace(
            ",", "").str.replace("£", "").astype(float)
        df["Paid in"] = df["Paid in"].str.replace(
            ",", "").str.replace("£", "").astype(float)
        return df
    except Exception as e:
        st.error(f"Error processing file:  {str(e)}")
        return None


def main():
    st.title("Nationwide Bank Statement Dashboard")

    uploaded_file = st.file_uploader(
        "Please upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        df["Category"] = "No Category"

        if df is not None:
            out_df = df[df["Paid out"].notnull()].copy()
            in_df = df[df["Paid in"].notnull()].copy()

            tab1, tab2 = st.tabs(["Money out", "Money In"])

            with tab1:
                filter_out_df = out_df.drop(columns=["Paid in", "Balance"])
                st.write(filter_out_df)
            with tab2:
                filter_in_df = in_df.drop(columns=["Paid out", "Balance"])
                st.write(filter_in_df)


main()
