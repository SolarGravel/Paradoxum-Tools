# streamlit run "c:/Users/three/Documents/Desenvolvimento/Paradoxum Helper/artifacts helper.py"

import streamlit as st
import pandas
import calculations
from pandas import DataFrame

artifacts_df: DataFrame = pandas.read_csv("artifacts.csv")

craft_ingredients: list[str] = []
ingredients_amount: list[int] = []
craft_prices: list[int] = []
additional_price: int = 0


def change_craft() -> None:
    global craft_prices
    global ingredients_amount

    craft_list = st.session_state["craft_list"]
    additional_price = st.session_state["additional"]

    if len(craft_list) != len(ingredients_amount):
        ingredients_amount = [1 for _ in range(len(craft_list))]

    craft_items: DataFrame = artifacts_df[artifacts_df["name"].isin(craft_list)]
    craft_prices = craft_items["price"].to_list()

    price_str: str = calculations.get_price_str(
        craft_items, ingredients_amount, additional_price
    )
    
    st.session_state["price_text"] = f"Prices: {price_str}"
    st.session_state["total_text"] = f"Total: {sum(craft_prices) + additional_price}"


st.title("New Artifact.", help="You need help making a new one?")
st.header("Craft", divider="gray")

with st.container(key="craft"):
    craft_ingredients = st.multiselect(
        "Craft Items:", key="craft_list", options=artifacts_df, on_change=change_craft
    )

    st.session_state["price_text"] = st.session_state.get("price_text", "Price:")
    st.session_state["total_text"] = st.session_state.get("total_text", "Total:")

    if craft_ingredients:
        st.write("Ingredients: ")

        for ingredient in craft_ingredients:
            ingredients_amount.append(st.number_input(ingredient, min_value=1, value=1, on_change=change_craft))

    additional_price = st.number_input("Additional Price:", key="additional", min_value=0, value=0, on_change=change_craft)

    prices_label = st.empty()
    prices_label.text(st.session_state["price_text"])
    
    total_label = st.empty()
    total_label.text(st.session_state["total_text"])
