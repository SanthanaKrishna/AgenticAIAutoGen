import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    'OPENAI_API_KEY'] = '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'

# Build AI Agent to analysis Image
async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    assistant = AssistantAgent(name="MultiModalAssistant", model_client=model_client)
    image = Image.from_file("D:\\Coding\\AI\\AI Agent\\course\\Taj_Mahal.jpeg")
    multimodal_message = MultiModalMessage(
        content=["what do you see in this image", image],
        source="user"
    )
    await Console(assistant.run_stream(task=multimodal_message))
    await model_client.close()


asyncio.run(main())
