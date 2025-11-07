# streamlit run "c:/Users/three/Documents/Desenvolvimento/Paradoxum Helper/artifacts.py"

import streamlit as st
import pandas
from pandas import DataFrame

artifacts_df: DataFrame = pandas.read_csv("artifacts.csv")


craft_items: list[str] = []
craft_prices: list[int] = []

def change_craft() -> None:
    global craft_prices
    
    craft_artifacts: DataFrame = artifacts_df[artifacts_df["name"].isin(st.session_state["craft_list"])]
    craft_prices = craft_artifacts["price"].to_list()
    st.session_state["price_text"] = f"Prices: {craft_prices}"

st.title("New Artifact.", help="You need help making a new one?")
st.header("Craft", divider="gray")

with st.container():
    craft_items = st.multiselect("Craft Items:", key="craft_list",options=artifacts_df, on_change=change_craft)
    
    st.session_state["price_text"] = st.session_state.get('price_text', 'Price: ')
    prices_label = st.empty()
    prices_label.write(st.session_state["price_text"])
