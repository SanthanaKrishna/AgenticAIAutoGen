import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    'OPENAI_API_KEY'] = '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'

# AI Agent with Human
async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4o")

    assistant = AssistantAgent(
        name="MathTutor",
        model_client=model_client,
        system_message="You are helpful math tutor. Help the user to solve math problem step by step."
                        "When the user says 'Thanks Done' or similar, acknowledge and say 'LESSON COMPLETE' to end session",
    )

    user_proxy = UserProxyAgent(name="Student")

    team = RoundRobinGroupChat(
        participants=[user_proxy, assistant],
        termination_condition= TextMentionTermination("LESSON COMPLETE")
    )

    await Console(team.run_stream(task="I need help with algebra problem, can you help me to solve 2*4+5"))

asyncio.run(main())


