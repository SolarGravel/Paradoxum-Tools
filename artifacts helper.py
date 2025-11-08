# streamlit run "c:/Users/three/Documents/Desenvolvimento/Paradoxum Helper/artifacts helper.py"

import streamlit as st
import pandas
import calculations
from pandas import DataFrame

artifacts_df: DataFrame = pandas.read_csv("artifacts.csv")

ingredients: list[str] = []
additional_price: int = 0


def change_craft() -> None:
    craft_ingredients: dict[str, dict[str, int]] = {}

    craft_list = st.session_state["craft_list"]
    additional_price = st.session_state["additional"]

    for ingredient in craft_list:
        craft_ingredients[ingredient] = {
            "amount": st.session_state.get(f"{ingredient}_amount", 1),
            "price": artifacts_df[artifacts_df["name"] == ingredient]["price"]
            .values[0]
            .item(),
        }

    price_str: str = calculations.get_price_str(craft_ingredients, additional_price)
    craft_prices: list[int] = [v["price"] * v["amount"] for v in craft_ingredients.values()]

    st.session_state["price_text"] = f"Prices: {price_str}"
    st.session_state["total_text"] = f"Total: {sum(craft_prices) + additional_price} J$"
    st.session_state["craft_ingredients"] = craft_ingredients


st.title("New Artifact.", help="You need help making a new one?")
st.header("Craft", divider="gray")

with st.container(key="craft"):
    st.multiselect(
        "Craft Items:", key="craft_list", options=artifacts_df, on_change=change_craft
    )

    st.session_state["price_text"] = st.session_state.get("price_text", "Price:")
    st.session_state["total_text"] = st.session_state.get("total_text", "Total:")
    st.session_state["craft_ingredients"] = st.session_state.get("craft_ingredients", {})

    craft_ingredients: dict[str, dict[str, int]] = st.session_state["craft_ingredients"]

    if craft_ingredients:
        st.write("Ingredients: ")

        for ingredient in craft_ingredients.keys():
            st.number_input(
                ingredient,
                key=f"{ingredient}_amount",
                min_value=1,
                value=1,
                on_change=change_craft,
            )

    additional_price = st.number_input(
        "Additional Price:",
        key="additional",
        min_value=0,
        value=0,
        on_change=change_craft,
    )

    prices_label = st.empty()
    prices_label.text(st.session_state["price_text"])

    total_label = st.empty()
    total_label.text(st.session_state["total_text"])
