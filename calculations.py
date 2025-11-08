stats_names: dict[str, str] = {
    "hp": "Max HP",
    "hp/s%": "HP Regeneration%",
    "protection": "Physicial Protection",
    "barrier": "Magic Barrier",
    "resilience": "Condition Resilience%",
    "ms": "Move Speed",
    "ms%": "Move Speed%",
    "runspd": "Run Speed%",
    "st/s": "Stamina Regeneration",
    "evasion": "Evasion%",
    "wp": "Weapon Power",
    "atk/s": "Attack Speed%",
    "atkrange": "Attack Range",
    "physvamp": "Life Steal%",
    "physpen": "Physical Penetration",
    "physpen%": "Physical Shreding%",
    "flux": "Flux",
    "spellrange": "Spell Range%",
    "cdr": "Cooldown Reduction",
    "magvamp": "Soul Steal%",
    "magpen": "Magic Penetration",
    "magpen%": "Magic Shreding%",
    "bless": "Blessing%",
    "sp/s": "Spirit Regeneration",
    "sp/s%": "Spirit Regeneration%",
    "energy": "Energy",
    "ammo": "Ammo%",
    "crit": "Critical Damage%",
    "luck": "Luck%"
}

def get_price_str(craft_items: dict[str, dict[str, int]], additional_price: int) -> str:
    result_str: str = ""

    for ingredient, info in craft_items.items():
        for _ in range(info["amount"]):
            result_str += f"*{ingredient}* ({info['price']} J$) + "

    result_str += f"{additional_price} J$"

    return result_str


if __name__ == "__main__":
    test_items = {"A": {"amount": 1, "price": 100}, "B": {"amount": 2, "price": 250}}

    print(get_price_str(test_items, 100))
