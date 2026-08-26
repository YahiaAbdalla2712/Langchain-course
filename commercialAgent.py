from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable

MAX_ITERATIONS = 10
MODEL = "qwen3:1.7b"

@tool
def get_product_price(product:str)->float:
    """Get all available products prices"""
    print(f"executing get_product_price(product = {product})")
    prices = {
        "laptop":1299.99,
        "headphones":149.95,
        "keyboard": 89.50
    }
    return prices.get(product,0)

@tool 
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


@traceable(name="LangChain Agent loop")
def run_agent(question:str):
    tools = [get_product_price, apply_discount]
    tools_dict = {
        t.name: t for t in tools
    }
    llm = init_chat_model(f"ollama:{MODEL}", temperature = 0)
    llm_with_tools = llm.bind_tools(tools)
    print(f"question:{question}")
    print("="*60)

    messages = [
        SystemMessage(
            content=(
                "You are a helpful shopping assistant." 
                "You have access to a product catalog tool"
                "and a discount tool.\n" 
                "STRICT RULES - You must follow these exactly:\n"
                "1-Never guess or assume any product price."
                "You MUST call get_product_price first to get the real prices.\n"
                "2- ONLY call apply_discount After you have received"
                "a Price from get_product_price. Pass the exact price"
                "returned by get_producrt_price -- do NOT pass a made-up number.\n"
                "3- DO NOT calculate discounts yourself using math."
                "Always use the apply_discount tool.\n"
                "4- If the user does not specify a discount tier,"
                "ask them which tier to use if user didn't mention -- do NOT assume one."
            )
        ),
        HumanMessage(
            content= question
        )
    ]

    for iteration in range(1,MAX_ITERATIONS+1):
        print(f"\n ---Iteration {iteration}---")
        ai_message = llm_with_tools.invoke(messages)
        tool_calls = ai_message.tool_calls
        if not tool_calls:
            print(f"\nFinal answer: {ai_message.content}")
            return ai_message.content
        tool_call = tool_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args",{})
        tool_call_id = tool_call.get("id")

        print(f"[Tool selceted {tool_name} with args: {tool_args}]")

        tool_to_use = tools_dict.get(tool_name)
        if tool_to_use is None:
            raise ValueError(f"Tool '{tool_name}' not found")
        observation = tool_to_use.invoke(tool_args)
        print(f" [Tool Result] {observation}")

        messages.append(ai_message)
        messages.append(ToolMessage(content = str(observation),tool_call_id=tool_call_id))

    print("ERROR: Max iterations reached without a final answer")
    return None    

if __name__ == "__main__":
    print("Hellp LangChain Agent(.bind_tools)!")
    print()
    result = run_agent("what is the price of a laptop after applying a gold discount")