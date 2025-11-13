import streamlit as st
import tools

stats: dict = st.session_state.get("stats", {})

st.session_state["stats"] = st.session_state.get("stats", {})


def on_change() -> None:
    damage_stats: dict = {"phys": {}, "mag": {}}
    defense_stats: dict = {}

    damage_stats = {
        "phys": {
            "damage": st.session_state.get("physdam_input", 0),
            "penetration": st.session_state.get("physpen_input", 0),
            "shredding": st.session_state.get("physpen%_input", 0.0) / 100,
        },
        "mag": {
            "damage": st.session_state.get("magdam_input", 0),
            "penetration": st.session_state.get("magpen_input", 0),
            "shredding": st.session_state.get("magpen%_input", 0.0) / 100,
        },
        "true": st.session_state.get("truedam_input"),
    }

    defense_stats = {
        "hp": st.session_state.get("hp_input", 0),
        "protection": st.session_state.get("phys_protec_input", 0),
        "barrier": st.session_state.get("mag_protec_input", 0),
        "resistance": st.session_state.get("resistance_input", 0.0) / 100,
    }

    st.session_state["stats"]["damage"] = damage_stats
    st.session_state["stats"]["defense"] = defense_stats


st.title("Damage Calculator")

with st.container(key="damage"):
    st.header("Damage", divider="grey")

    phys_col, mag_col = st.columns(2)

    with phys_col:
        st.number_input(
            "Physical Damage:",
            key="physdam_input",
            min_value=0,
            value=0,
            on_change=on_change,
            width=200,
            icon=":material/surgical:",
        )
        st.number_input(
            "Physical Penetration:",
            key="physpen_input",
            min_value=0,
            value=0,
            on_change=on_change,
            width=200,
            icon=":material/link_off:",
        )
        st.number_input(
            "Physical Shredding:",
            key="physpen%_input",
            min_value=0.0,
            value=0.0,
            on_change=on_change,
            width=200,
            icon=":material/percent:",
        )

    with mag_col:
        st.number_input(
            "Magic Damage:",
            key="magdam_input",
            min_value=0,
            value=0,
            on_change=on_change,
            width=200,
            icon=":material/visibility:",
        )
        st.number_input(
            "Magic Penetration:",
            key="magpen_input",
            min_value=0,
            value=0,
            on_change=on_change,
            width=200,
            icon=":material/visibility_off:",
        )
        st.number_input(
            "Magic Shredding:",
            key="magpen%_input",
            min_value=0.0,
            value=0.0,
            on_change=on_change,
            width=200,
            icon=":material/percent:",
        )

    st.number_input(
        "True Damage:",
        key="truedam_input",
        min_value=0,
        value=0,
        on_change=on_change,
        width=200,
        icon=":material/circle:",
    )


with st.container(key="defense"):
    st.header("Defense", divider="grey")

    st.number_input(
        "Max HP:",
        key="hp_input",
        min_value=0,
        value=0,
        on_change=on_change,
        width=200,
        icon=":material/health_cross:",
    )

    phys_col, mag_col = st.columns(2)

    with phys_col:
        st.number_input(
            "Physical Protection:",
            key="phys_protec_input",
            min_value=0,
            value=0,
            on_change=on_change,
            width=200,
            icon=":material/health_and_safety:",
        )

    with mag_col:
        st.number_input(
            "Magic Barrier:",
            key="mag_protec_input",
            min_value=0,
            value=0,
            on_change=on_change,
            width=200,
            icon=":material/arming_countdown:",
        )

    st.number_input(
        "Resistance:",
        key="resistance_input",
        value=0.0,
        on_change=on_change,
        width=200,
        icon=":material/percent:",
    )

with st.container(key="result"):
    st.header("Result", divider="grey")

    with st.expander("info"):
        if "defense" in stats:
            defensive_stats: dict = stats["defense"]

            st.write(
                f"- **Physical Protection%**: {round(tools.get_percent_protection(defensive_stats['protection']) * 100, 2)}%"
            )
            st.write(
                f"- **Effective Physical HP**: {tools.get_effective_hp(defensive_stats['hp'], defensive_stats['protection'])}"
            )
            
            st.write(
                f"- **Magic Barrier%**: {round(tools.get_percent_protection(defensive_stats['barrier']) * 100, 2)}%"
            )
            st.write(
                f"- **Effective Magic HP**: {tools.get_effective_hp(defensive_stats['hp'], defensive_stats['barrier'])}"
            )

    with st.expander("dict"):
        st.write(stats)
