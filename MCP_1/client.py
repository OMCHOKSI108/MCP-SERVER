from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()


import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"], ## correct absoult path
                "transport":"stdio"

            }, 

            "weather":{
               "url" :"http://localhost:8000/mcp", ##ensure server is runinig 
               "transport":"streamable_http",
            }
        }
    )

    import os
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()

    model = ChatGroq(model="deepseek-r1-distill-llama-70b")

    agent = create_react_agent(
        model,tools
    )

    # Math query
    print("\n" + "="*80)
    print("MATH QUERY: what's (3+5)x12 ?")
    print("="*80)
    
    math_response = await agent.ainvoke(
        {"messages" : [{"role":"user","content":"what's (3+5)x12 ?"}]}
    )
    
    print(math_response['messages'][-1].content)
    print("="*80 + "\n")

    # Weather query
    print("\n" + "="*80)
    print("WEATHER QUERY: what is the weather in surat")
    print("="*80)
    
    try:
        weather_response = await agent.ainvoke(
            {"messages": [{"role":"user","content":"what is the weather in surat"}]},
            {"recursion_limit": 10}  # Limit recursion to fail faster if server isn't running
        )
        print(weather_response['messages'][-1].content)
    except Exception as e:
        print(f"Error: Could not get weather response.")
        print(f"Make sure the weather server is running with: python weather.py")
        print(f"Details: {e}")
    
    print("="*80 + "\n")

asyncio.run(main())    