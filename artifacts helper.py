# streamlit run "c:/Users/three/Documents/Desenvolvimento/Paradoxum Helper/artifacts helper.py"
# streamlit run "c:/Users/12725158143/Documents/Github/Paradoxum-Helper/artifacts helper.py"

import streamlit as st
import pandas
import calculations
from pandas import DataFrame
from math import ceil

artifacts_df: DataFrame = pandas.read_csv("artifacts.csv")
stats_df: DataFrame = pandas.read_csv("stats.csv")

ingredients: list[str] = []
additional_price: int = 0
item_stats: dict[str, float] = {}


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
    craft_prices: list[int] = [
        v["price"] * v["amount"] for v in craft_ingredients.values()
    ]

    total: int = sum(craft_prices) + additional_price

    st.session_state["price_text"] = f"Craft: {price_str}"
    st.session_state["total_text"] = (
        f"***Cost***: {total} J$ *({ceil(total / 2)} J$ Sell)*"
    )
    st.session_state["craft_ingredients"] = craft_ingredients


st.title("New Artifact.", help="You need help making a new one?")

with st.container(key="craft"):
    st.header("Craft", divider="gray")

    st.multiselect(
        "Craft Items:", key="craft_list", options=artifacts_df, on_change=change_craft
    )

    st.session_state["price_text"] = st.session_state.get("price_text", "Price:")
    st.session_state["total_text"] = st.session_state.get("total_text", "Total:")
    st.session_state["craft_ingredients"] = st.session_state.get(
        "craft_ingredients", {}
    )

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
                icon=":material/diamond_shine:",
            )

    additional_price = st.number_input(
        "Additional Price:",
        key="additional",
        min_value=0,
        value=0,
        on_change=change_craft,
        icon=":material/money_bag:",
    )

    prices_label = st.empty()
    prices_label.text(st.session_state["price_text"])

    total_label = st.empty()
    total_label.text(st.session_state["total_text"])

with st.container(key="stats"):
    st.header("Stats", divider="gray")

    for ingredient in craft_ingredients:
        artifact: DataFrame = artifacts_df[artifacts_df["name"] == ingredient]

        stats_names = dict(zip(stats_df["stat"], stats_df["name"]))
        
        for stat, name in stats_names.items():
            if not pandas.isna(artifact[stat].values[0]):
                if name in item_stats:
                    item_stats[name] += artifact[stat].values[0].item()
                else:
                    item_stats[name] = artifact[stat].values[0].item()

        for stat, value in item_stats.items():
            stat_col, input_col, total_col = st.columns(3, vertical_alignment="center")

            with stat_col:
                st.write(f"**{stat}**: {value}")
            
            with input_col:
                additional_stat = st.number_input(
                    "Additional Stat",
                    key=f"{stat}_stat",
                    min_value=0.0,
                    value=0.0,
                    on_change=change_craft,
                    icon=f":material/{stats_df[stats_df['name'] == stat]['icon'].values[0]}:",
                )
            
            with total_col:
                st.write(f"**{value + additional_stat}**")
