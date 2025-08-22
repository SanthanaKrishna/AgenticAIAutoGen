import asyncio
import os
from turtle import Terminator

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

os.environ[
    'OPENAI_API_KEY'] = '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'


# A dd MCP tooling support to Agent
async def main():
    # configuration for file system mcp server
    filesystem_mcp_server_params = StdioServerParams(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "C:\\Users\\santh\\Desktop"
        ],
        read_timeout_seconds=60
    )

    # start mcp server by create instance of mcp workbench class
    # to start which server, we are passing params as 'filesystem_mcp_server_params'
    fs_workbench = McpWorkbench(filesystem_mcp_server_params)

    async with fs_workbench:
        model_client = OpenAIChatCompletionClient(model="gpt-4o")

        math_tutor = AssistantAgent(
            name="MathTutor",
            model_client=model_client,
            workbench=fs_workbench,  # workbench is a tooling support adding to the agent
            system_message="You are helpful math tutor. Help the user to solve math problem step by step."
                           "You have to access to file system to create file for student learning"
                           "When the user says 'Thanks Done' or similar, acknowledge and say 'LESSON COMPLETE' to end session"
        )

    user_proxy = UserProxyAgent(name="Student")

    # Create team with text termination
    team = RoundRobinGroupChat(
        participants=[user_proxy, math_tutor],
        termination_condition=TextMentionTermination("LESSON COMPLETE")
    )

    await Console(team.run_stream(
        task="I need help with algebra problem."
            "Tutor feel free to create files to help with student learning."
    ))

    await model_client.close()

asyncio.run(main())