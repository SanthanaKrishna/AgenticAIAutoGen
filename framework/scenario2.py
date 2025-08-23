from autogen_ext.models.openai import OpenAIChatCompletionClient

from framework.agentFactory import AgentFactory


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    factory = AgentFactory(model_client)
    database_agent = factory.create_database_agent("You are database specialist")