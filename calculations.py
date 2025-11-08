from pandas import DataFrame

def get_price_str(craft_items: DataFrame, amounts: list[int], additional_price: int) -> str:
    result_str: str = ""
    
    ingredient_names = craft_items["name"].to_list()
    ingredient_prices = craft_items["price"].to_list()
    
    for i, item in enumerate(ingredient_names):
        for _ in range(amounts[i]):
            result_str += f"*{item}* ({ingredient_prices[i]} J$) + "
    
    result_str += f"{additional_price} J$"
    
    return result_str


if __name__ == "__main__":
    test_items = DataFrame({
        "name": ["A", "B"],
        "price": [100, 200]
    })
    
    print(get_price_str(test_items, [1, 2], 100))