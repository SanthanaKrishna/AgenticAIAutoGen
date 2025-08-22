import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    'OPENAI_API_KEY'] = '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'

# multi AI Agent Interaction using SelectorGroupChat
async def main():
    #create first assistant agent
    model_client = OpenAIChatCompletionClient(model="gpt-4o")

    researcher = AssistantAgent(
        name="ResearchAgent",
        model_client=model_client,
        system_message="You are a researcher, Your role is to gather information and provide research findings ONLY."
                        "Do not write article or create content - just provide research data and facts"
    )

    writer = AssistantAgent(
        name="WriterAgent",
        model_client=model_client,
        system_message="You are a writer. Your role is to take research information and create well-written articles."
                        "wait for research to be provided, then write the content."
    )

    critic = AssistantAgent(
        name="CriticAgent",
        model_client=model_client,
        system_message="You are a critic. Review written content and provide feedback."
                        "Say 'TERMINATE' when satisfied with the final result."
    )

    text_termination = TextMentionTermination("TERMINATE")
    max_message_termination = MaxMessageTermination(max_messages=15)

    termination_condition = text_termination | max_message_termination

    team = SelectorGroupChat(
        participants=[critic, writer, researcher],
        model_client=model_client,
        allow_repeated_speaker=True,
        termination_condition=termination_condition,
    )

    await Console(team.run_stream(task="Research renewable energy trends and write a brief article about the future of solar power."))
    await model_client.close()


asyncio.run(main())