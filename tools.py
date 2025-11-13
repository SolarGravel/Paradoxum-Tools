import pandas
from pandas import DataFrame

stats_df: DataFrame = pandas.read_csv("data/stats.csv")

def get_price_str(craft_items: dict[str, dict[str, int]], additional_price: int) -> str:
    result_str: str = ""

    for ingredient, info in craft_items.items():
        for _ in range(info["amount"]):
            result_str += f"*{ingredient}* ({info['price']} J$) + "

    result_str += f"{additional_price} J$"

    return result_str

def get_stat_price(stat: str, value: float) -> float:
    stat_df = stats_df[stats_df["name"] == stat]
    
    return int(stat_df["price"].values[0]) * value

if __name__ == "__main__":
    print(get_stat_price("Weapon Power", 60))
