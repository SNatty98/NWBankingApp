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
        df["Paid out"] = df["Paid out"].str.replace(
            ",", "").str.replace("£", "").astype(float)
        df["Paid in"] = df["Paid in"].str.replace(
            ",", "").str.replace("£", "").astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")
        st.write(df)
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


main()
