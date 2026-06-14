from agents import Agent, Runner, OpenAIChatCompletionsModel, set_default_openai_client
from openai import AsyncOpenAI
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("API", "")

client = AsyncOpenAI(
    api_key=os.getenv("API"),
    base_url=os.getenv("BASE"),
)

set_default_openai_client(client)

from agents.mcp import MCPServerStdio

sandbox_path = os.path.join(os.getcwd(), "sandbox")
linkedin_file = os.path.join(sandbox_path, "linkedin.py")  
browse_tools = {
    "command": "npx",
    "args": ["@playwright/mcp@latest"],
    "cwd": sandbox_path  }


file_tools = {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path],
    "cwd": sandbox_path
}

instructions = f"""
You are a job research assistant with browser and filesystem access.

STEP BY STEP:
1. Navigate to: https://www.linkedin.com/jobs/search/?keywords=AI+internship&f_JT=I&location=India
2. Wait for the page to load
3. Take a snapshot of the page (accessibility tree)
4. READ the snapshot carefully and find all links containing '/jobs/view/'
5. Extract from each link:
   - The href URL
   - The link text (job title)
   - Nearby company name and location text
6. Repeat for:
   - https://www.linkedin.com/jobs/search/?keywords=Machine+Learning+internship&f_JT=I
   - https://www.linkedin.com/jobs/search/?keywords=Backend+internship&f_JT=I
7. Scroll down and take new snapshots to load more jobs
8. Categorize and save all to: {linkedin_file}

HOW TO READ SNAPSHOT:
- Look for lines like: link "Job Title" [href="/jobs/view/XXXXXXX/"]
- The number in /jobs/view/XXXXXXX/ is the job ID
- Full URL = https://www.linkedin.com/jobs/view/XXXXXXX/
- Company and location appear as text near the link

OUTPUT FORMAT to save in {linkedin_file}:
ai_internships = [
    {{"title": "...", "company": "...", "location": "...", "url": "https://www.linkedin.com/jobs/view/..."}},
]
ml_internships = [
    {{"title": "...", "company": "...", "location": "...", "url": "https://www.linkedin.com/jobs/view/..."}},
]
backend_internships = [
    {{"title": "...", "company": "...", "location": "...", "url": "https://www.linkedin.com/jobs/view/..."}},
]

STRICT RULES:
- READ every snapshot carefully line by line
- Only collect links with '/jobs/view/' in href
- Scroll and snapshot multiple times to get at least 10 jobs per category
- Save file to EXACT path: {linkedin_file}
- Do NOT save to mistake.py or any other file
"""

async def Tool_call():
    async with MCPServerStdio(params=file_tools, client_session_timeout_seconds=60) as filesys_tools:
        async with MCPServerStdio(params=browse_tools, client_session_timeout_seconds=60) as browser_tools:
            agent = Agent(
                name="LinkedIn Internship Scraper",
                instructions=instructions,
                model=OpenAIChatCompletionsModel(
                    model="gemini-2.5-flash",
                    openai_client=client
                ),
                mcp_servers=[filesys_tools, browser_tools]
            )

            result = await Runner.run(
                agent,
                f"""
                Browse LinkedIn and collect internship links for AI, ML and Backend.

                Visit these URLs one by one:
                - https://www.linkedin.com/jobs/search/?keywords=AI+internship&f_JT=I&location=India
                - https://www.linkedin.com/jobs/search/?keywords=Machine+Learning+internship&f_JT=I&location=India
                - https://www.linkedin.com/jobs/search/?keywords=Backend+internship&f_JT=I&location=India

                For each page:
                - Take a snapshot and read all links containing /jobs/view/
                - Scroll down 3-4 times and take new snapshots each time
                - Collect title, company, location and full LinkedIn URL

                Save ONLY to: {linkedin_file}
                """,
                max_turns=60
            )

            print("=== FINAL OUTPUT ===")
            print(result.final_output)
            if not os.path.exists(linkedin_file):
                if result.final_output:
                    with open(linkedin_file, "w", encoding="utf-8") as f:
                        f.write(result.final_output)
                    print(f"✅ Manually saved to {linkedin_file}")
                else:
                    print("❌ Agent returned no output — nothing saved")
            else:
                print(f"✅ File already saved by agent at {linkedin_file}")

asyncio.run(Tool_call())