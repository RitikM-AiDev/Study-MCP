from agents import Agent,Runner
from dotenv import load_dotenv
from agents.mcp import MCPServerStdio
import os

load_dotenv()



#--------------------------INTERNET TOOL TO FETCH FROM INTERNET-----------------------------------------------------


fetch_params = {"command" : "uvx", "args" : ["mcp-server-fetch"]}

async def mcp_tool_fetch(fetch_params):
    async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=30) as server:
        fetch_tools = await server.list_tools()
        for tool in fetch_tools:
            print(tool.name, tool.description)



#-------------------------- BROWSER TOOLS -----------------------------------------------------

browser_tools = {"command" : "npx" , "args" : ["@playwright/mcp@latest"]}
async def browser_tool(fetch_params):
    async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=30) as server:
        fetch_tools = await server.list_tools()
        for tool in fetch_tools:
            print(tool.name, tool.description)


#------------------------------------------FILE SYSTEM TOOLS-----------------------------------------------------



sandbox_path=os.path.join(os.getcwd(),"sandbox")
file_system_tools={"command" : "npx" , "args" : ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path]}
async def files_tool(fetch_params):
    async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=30) as server:
        fetch_tools = await server.list_tools()
        for tool in fetch_tools:
            print(tool.name, tool.description)

#--------------------------------------------------------MEMORY-----------------------------
import asyncio
asyncio.run(files_tool(file_system_tools))
