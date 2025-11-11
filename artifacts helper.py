# streamlit run "c:/Users/three/Documents/Desenvolvimento/Paradoxum-Helper/artifacts helper.py"
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
ingredient_stats: dict[str, float] = {}
additional_stats: dict[str, float] = {}

st.session_state["price_text"] = st.session_state.get("price_text", "Price:")
st.session_state["total_price"] = st.session_state.get("total_price", 0)
st.session_state["craft_ingredients"] = st.session_state.get("craft_ingredients", {})

craft_ingredients: dict[str, dict[str, int]] = st.session_state["craft_ingredients"]
extra_stats: list[str] = st.session_state.get("add_stats", [])


def change_item() -> None:
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

    st.session_state["price_text"] = f"Craft: {price_str}"
    st.session_state["total_price"] = sum(craft_prices) + additional_price
    st.session_state["craft_ingredients"] = craft_ingredients


st.title("New Artifact.", help="You need help making a new one?")

with st.container(key="stats"):
    st.header("Stats", divider="gray")

    for ingredient in craft_ingredients:
        for i in range(craft_ingredients[ingredient]["amount"]):
            artifact: DataFrame = artifacts_df[artifacts_df["name"] == ingredient]

            stats_names = dict(zip(stats_df["stat"], stats_df["name"]))

            for stat, name in stats_names.items():
                if not pandas.isna(artifact[stat].values[0]):
                    if name in ingredient_stats:
                        ingredient_stats[name] += artifact[stat].values[0].item()
                    else:
                        ingredient_stats[name] = artifact[stat].values[0].item()

    for stat, value in ingredient_stats.items():
        if stat in extra_stats:
            extra_stats.remove(stat)

        stat_col, input_col, total_col = st.columns(
            3, vertical_alignment="center", width=550
        )
        if stat == "Move Speed":
            with stat_col:
                st.write(f"**{stat}**: {value}")

            with input_col:
                additional_stats[stat] = st.number_input(
                    "Additional Stat",
                    key=f"{stat}_stat",
                    min_value=0.0,
                    value=0.0,
                    on_change=change_item,
                    icon=f":material/{stats_df[stats_df['name'] == stat]['icon'].values[0]}:",
                )

            with total_col:
                st.write(f"Total: **{value + additional_stats[stat]}**")
        elif stat[-1] == "%":
            with stat_col:
                st.write(f"**{stat}**: {value * 100}%")

            with input_col:
                additional_stats[stat] = st.number_input(
                    "Additional Stat",
                    key=f"{stat}_stat",
                    min_value=0.0,
                    value=0.0,
                    on_change=change_item,
                    icon=f":material/{stats_df[stats_df['name'] == stat]['icon'].values[0]}:",
                )

            with total_col:
                st.write(f"Total: **{value * 100 + additional_stats[stat]}%**")
        else:
            with stat_col:
                st.write(f"**{stat}**: {int(value)}")

            with input_col:
                additional_stats[stat] = st.number_input(
                    "Additional Stat",
                    key=f"{stat}_stat",
                    min_value=0,
                    value=0,
                    on_change=change_item,
                    icon=f":material/{stats_df[stats_df['name'] == stat]['icon'].values[0]}:",
                )

            with total_col:
                st.write(f"Total: **{int(value + additional_stats[stat])}**")

    for stat in extra_stats:
        stat_col, input_col, total_col = st.columns(
            3, vertical_alignment="center", width=550
        )

        if stat == "Move Speed":
            with stat_col:
                st.write(f"**{stat}**: 0.0")

            with input_col:
                additional_stats[stat] = st.number_input(
                    "Additional Stat",
                    key=f"{stat}_stat",
                    min_value=0.0,
                    value=0.0,
                    on_change=change_item,
                    icon=f":material/{stats_df[stats_df['name'] == stat]['icon'].values[0]}:",
                )

            with total_col:
                st.write(f"Total: **{additional_stats[stat]}**")
        elif stat[-1] == "%":
            with stat_col:
                st.write(f"**{stat}**: 0%")

            with input_col:
                additional_stats[stat] = st.number_input(
                    "Additional Stat",
                    key=f"{stat}_stat",
                    min_value=0.0,
                    value=0.0,
                    on_change=change_item,
                    icon=f":material/{stats_df[stats_df['name'] == stat]['icon'].values[0]}:",
                )

            with total_col:
                st.write(f"Total: **{additional_stats[stat]}%**")
        else:
            with stat_col:
                st.write(f"**{stat}**: 0")

            with input_col:
                additional_stats[stat] = st.number_input(
                    "Additional Stat",
                    key=f"{stat}_stat",
                    min_value=0,
                    value=0,
                    on_change=change_item,
                    icon=f":material/{stats_df[stats_df['name'] == stat]['icon'].values[0]}:",
                )

            with total_col:
                st.write(f"Total: **{int(additional_stats[stat])}**")

    stat_prices: list[float] = []

    if ingredient_stats or additional_stats:
        st.text("### Stat Price\n- *The price of each stat:*")

        for stat, value in ingredient_stats.items():
            stat_prices.append(
                calculations.get_stat_price(stat, value + additional_stats[stat])
            )
            
            if stat in additional_stats:
                del additional_stats[stat]

            st.text(f"  - *{stat}: {stat_prices[len(stat_prices) - 1]} J$*")

        for stat in additional_stats:
            stat_prices.append(
                calculations.get_stat_price(stat, additional_stats[stat])
            )

            st.text(f"  - *{stat}: {stat_prices[len(stat_prices) - 1]} J$*")

    total_price: int = st.session_state["total_price"]
    
    if total_price != 0:
        efficiency: float = sum(stat_prices) / st.session_state["total_price"]
        
        st.text(f"- *Total: {sum(stat_prices)} J$. Efficiency of {round(efficiency * 100, 2)}%*")

    st.header("Additional Stats")
    st.multiselect(
        "Stat:", key="add_stats", options=stats_df["name"], on_change=change_item
    )

with st.container(key="craft"):
    st.header("Craft", divider="gray")

    st.multiselect(
        "Craft Items:", key="craft_list", options=artifacts_df, on_change=change_item
    )

    if craft_ingredients:
        st.write("Ingredients: ")

        for ingredient in craft_ingredients.keys():
            st.number_input(
                ingredient,
                key=f"{ingredient}_amount",
                min_value=1,
                value=1,
                on_change=change_item,
                icon=":material/diamond_shine:",
            )

    additional_price = st.number_input(
        "Additional Price:",
        key="additional",
        min_value=0,
        value=0,
        on_change=change_item,
        icon=":material/money_bag:",
    )

    prices_label = st.empty()
    prices_label.text(st.session_state["price_text"])

    total_label = st.empty()
    total_label.text(f"***Cost***: {total_price} J$ *({ceil(total_price / 2)} J$ Sell)*")