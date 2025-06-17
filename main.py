import os
import streamlit as st
import pandas as pd
import plotly.express as px
import json


st.set_page_config(page_title="Nationwide Bank Statement App",
                   layout="wide")

# Initialize categories.
if "categories" not in st.session_state:
    st.session_state.categories = {
        "Uncategorised": []
    }


if os.path.exists("categories.json"):
    with open("categories.json", "r") as f:
        st.session_state.categories = json.load(f)


def save_categories():
    with open("categories.json", "w") as f:
        json.dump(st.session_state.categories, f)


def categorise_transactions(df):
    df["Category"] = "No Category"

    for category, keywords in st.session_state.categories.items():
        if category == "No Category" or not keywords:
            continue

        lowered_keywords = [keyword.lower().strip() for keyword in keywords]

        for idx, row in df.iterrows():
            desc = row["Description"].lower()
            if desc in lowered_keywords:
                df.at[idx, "Category"] = category
    return df


def load_transactions(file):
    try:
        df = pd.read_csv(file, encoding='latin-1', skiprows=3)
        df.columns = [col.strip() for col in df.columns]
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")
        df["Paid out"] = df["Paid out"].str.replace(
            ",", "").str.replace("£", "").astype(float)
        df["Paid in"] = df["Paid in"].str.replace(
            ",", "").str.replace("£", "").astype(float)

        return categorise_transactions(df)
    except Exception as e:
        st.error(f"Error processing file:  {str(e)}")
        return None


def add_keyword_category(category, keyword):
    keyword = keyword.strip()
    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    return False


def main():
    st.title("Nationwide Bank Statement Dashboard")

    uploaded_file = st.file_uploader(
        "Please upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        if df is not None:

            out_df = df[df["Paid out"].notnull()].copy()
            in_df = df[df["Paid in"].notnull()].copy()

            st.session_state.out_df = out_df.copy()

            tab1, tab2 = st.tabs(["Money out", "Money In"])

            with tab1:
                st.subheader("Your Expenses")

                new_category = st.text_input("Enter a Category!")
                add_button = st.button("Add Category")

                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.rerun()

                # filter_out_df = out_df.drop(columns=["Paid in", "Balance"])
                st.subheader("Your Expenses")

                # Display specific columns and modify them;
                # Users can also select existing categories from the .JSON
                edited_df = st.data_editor(
                    st.session_state.out_df[[
                        "Date", "Transaction type", "Description", "Paid out", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Paid in": st.column_config.NumberColumn("Paid in", format="%,.2f GBP"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(
                                st.session_state.categories.keys())
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )

                save_button = st.button("Apply Changes", type="primary")
                if save_button:
                    pass

            with tab2:
                filter_in_df = in_df.drop(columns=["Paid out", "Balance"])
                st.write(filter_in_df)


main()
