import asyncio
import os

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    'OPENAI_API_KEY'] = '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'


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o"
    )

    web_surfer_agent = MultimodalWebSurfer(
        name= "WebSurfer",
        model_client=model_client,
        headless= False,
        animate_actions=True
    )

    team = RoundRobinGroupChat(
        participants=[web_surfer_agent],
        max_turns=3
    )

    await Console(team.run_stream(task="Navigate to Google and search for 'AutoGen framework Python'. Then summarize what you find"))
    await web_surfer_agent.close()
    await model_client.close()

asyncio.run(main())