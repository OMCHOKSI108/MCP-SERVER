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

    # Minimal examples
    resp = await agent.ainvoke({"messages":[{"role":"user","content":"what is (3+5)*12?"}]})
    print(resp["messages"][-1].content)

    try:
        resp = await agent.ainvoke({"messages":[{"role":"user","content":"what is the weather in surat?"}]})
        print(resp["messages"][-1].content)
    except Exception:
        print("Weather server unavailable")

asyncio.run(main())    