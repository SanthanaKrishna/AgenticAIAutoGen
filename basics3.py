import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    'OPENAI_API_KEY'] = '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'

# multi AI Agent Interaction
async def main():
    #create first assistant agent
    model_client = OpenAIChatCompletionClient(model="gpt-4o")

    agent1 = AssistantAgent(
        name="MathTeacher",
        model_client=model_client,
        system_message="You are a math teacher, Explain concepts clearly and ask follow-up question"
    )
    agent2 = AssistantAgent(
        name="Student",
        model_client=model_client,
        system_message="You are a curious student. Ask question and show your thinking process"
    )

    team = RoundRobinGroupChat(
        participants=[agent1, agent2],
        termination_condition=MaxMessageTermination(max_messages=6)
    )
    await Console(team.run_stream(task="Let's discuss what is multiplication and how its works"))
    await model_client.close()


asyncio.run(main())