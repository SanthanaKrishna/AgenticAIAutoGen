import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


os.environ['OPENAI_API_KEY'] = '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'


async def main():
    print("Hello World")
    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o"
    )
    assistant = AssistantAgent(name="assistant", model_client= openai_model_client)
    await Console(assistant.run_stream(task="What is 25 * 8?"))
    await openai_model_client.close()

asyncio.run(main())
