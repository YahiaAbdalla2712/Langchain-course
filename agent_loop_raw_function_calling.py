from dotenv import load_dotenv
load_dotenv()

import ollama
from langsmith import traceable


@traceable(run_type = "tool")
def get_product_price(product:str)->float:
    """Get all available products prices"""
    print(f"executing get_product_price(product = {product})")
    prices = {
        "laptop":1299.99,
        "headphones":149.95,
        "keyboard": 89.50
    }
    return prices.get(product,0)


@traceable(run_type = "tool")
def apply_discount(price:float,discount_tier:str)->float:
    """get the value percentage of the discount tier and return the final price"""
    print(f"executing apply_discount(price = {price}, discount_tier = {discount_tier})")
    discount_percentages = {
        "bronze":5,
        "silver":12,
        "gold":23
    }
    discount = discount_percentages.get(discount_tier,0)
    return round(price*(1-discount/100),2)



tools_for_llm = [
    {
        "type":"function",
        "function":{
          "name":"get_product_price",
          "description":"Get all available products prices",
          "parameters":{
              "type":"object",
              "properties":{
                  "product":{
                      "type":"string",
                      "description":"The Product name, e.g 'laptop', 'headphones', 'keyboard'",
                  },
              },
              "required":["product"],
          },
        },
    },
]