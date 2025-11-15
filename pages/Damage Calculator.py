import streamlit as st
import tools
from tools import Damage, DamageStats, DefenseStats, BasicAtkStats, DamageType


st.session_state["stats"] = st.session_state.get(
    "stats",
    {"damage": Damage(), "defense": DefenseStats(), "dps": BasicAtkStats()},
)

stats: dict = st.session_state.get("stats", {})


def on_change() -> None:
    damage_stats: Damage = Damage(
        physic=DamageStats(
            damage=st.session_state.get("physdam_input", 0),
            penetration=st.session_state.get("physpen_input", 0),
            shredding=st.session_state.get("physpen%_input", 0.0) / 100,
        ),
        magic=DamageStats(
            damage=st.session_state.get("magdam_input", 0),
            penetration=st.session_state.get("magpen_input", 0),
            shredding=st.session_state.get("magpen%_input", 0.0) / 100,
        ),
        true=st.session_state.get("truedam_input", 0),
    )

    defense_stats: DefenseStats = DefenseStats(
        hp=st.session_state.get("hp_input", 0),
        protection=st.session_state.get("phys_protec_input", 0),
        barrier=st.session_state.get("mag_protec_input", 0),
        resistance=st.session_state.get("resistance_input", 0.0) / 100,
    )

    basic_stats: BasicAtkStats = BasicAtkStats(
        dps_damage={
           DamageType.PHYSICAL: st.session_state.get("dps_damage_input", 0),
           DamageType.MAGIC: st.session_state.get("mag_dps_damage_input", 0),
           DamageType.TRUE: st.session_state.get("true_dps_damage_input", 0),
        },
        atk_speed=st.session_state.get("dps_input", 0),
        effect=st.session_state.get("dps_efect_input", 100) / 100,
    )

    st.session_state["stats"]["damage"] = damage_stats
    st.session_state["stats"]["defense"] = defense_stats
    st.session_state["stats"]["dps"] = basic_stats


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


with st.container(key="dps"):
    st.header("Basic Attack", divider="grey")

    phys_col, mag_col = st.columns(2)
    
    with phys_col:
        st.number_input(
            "Physic Damage:",
            key="dps_damage_input",
            min_value=0,
            value=0,
            on_change=on_change,
            width=200,
            icon=":material/surgical:",
        )
    
    with mag_col:
        st.number_input(
            "Magic Damage:",
            key="mag_dps_damage_input",
            min_value=0,
            value=0,
            on_change=on_change,
            width=200,
            icon=":material/visibility:",
        )
    
    st.number_input(
        "True Damage:",
        key="true_dps_damage_input",
        min_value=0,
        value=0,
        on_change=on_change,
        width=200,
        icon=":material/circle:",
    )

    st.number_input(
        "Attack Speed:",
        key="dps_input",
        min_value=0.0,
        value=0.0,
        on_change=on_change,
        width=200,
        icon=":material/speed:",
    )

    st.number_input(
        "Effectiveness:",
        key="dps_efect_input",
        min_value=0.0,
        value=100.0,
        on_change=on_change,
        width=200,
        icon=":material/percent:",
    )
    
    st.write(f"DPS: {tools.get_dps(stats['dps'])}")


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

    defense_stats: DefenseStats = stats["defense"]
    damage_stats: Damage = stats["damage"]
    basic_atk_stats: BasicAtkStats = stats["dps"]

    damages = tools.get_damages(damage_stats, defense_stats, basic_atk_stats)

    total_damage = sum(damages)

    st.write(f"*Physical Damage*: {damages[0]}")
    st.write(f"*Magic Damage*: {damages[1]}")
    st.write(f"*True Damage*: {damages[2]}")
    st.write(f"**Total Damage**: {total_damage}\n")

    remainging_hp: str | float = defense_stats.hp - total_damage
    remainging_hp = "**0**" if remainging_hp <= 0 else remainging_hp

    st.write(f"Remaining HP: {remainging_hp}")

    with st.expander("info"):
        effective_protection = round(
            tools.get_effective_protection(
                defense_stats.protection,
                damage_stats.physic.penetration,
                damage_stats.physic.shredding,
            )
        )

        effective_barrier = round(
            tools.get_effective_protection(
                defense_stats.barrier,
                damage_stats.magic.penetration,
                damage_stats.magic.shredding,
            )
        )

        st.write(
            f"- **Physical Protection%**: {round(tools.get_percent_protection(effective_protection) * 100, 2)}%"
        )

        st.write(
            f"- **Effective Physical HP**: {tools.get_effective_hp(defense_stats.hp, effective_protection)}"
        )

        st.write(
            f"- **Magic Barrier%**: {round(tools.get_percent_protection(effective_barrier) * 100, 2)}%"
        )
        st.write(
            f"- **Effective Magic HP**: {tools.get_effective_hp(defense_stats.hp, effective_barrier)}"
        )

    with st.expander("dict"):
        st.write(stats)
