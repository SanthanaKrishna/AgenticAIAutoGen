import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

os.environ['OPENAI_API_KEY'] = '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'
os.environ['JIRA_URL'] = 'https://rahulshettyacademy12.atlassian.net/'
os.environ['JIRA_USERNAME'] = 'rahulshettyacademy@gmail.com'
os.environ['JIRA_API_KEY'] = ''
os.environ['JIRA_PROJECTS_FILTER']= 'CRED'

async def main():
    modal_client= OpenAIChatCompletionClient(model="gpt-4o")

    # jira mcp server
    jira_server_params = StdioServerParams(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-e", f"JIRA_URL={os.environ['JIRA_URL']}",
            "-e", f"JIRA_USERNAME={os.environ['JIRA_USERNAME']}",
            "-e", f"JIRA_API_TOKEN={os.environ['JIRA_API_KEY']}",
            "-e", f"JIRA_PROJECTS_FILTER={os.environ['JIRA_PROJECTS_FILTER']}",
            "ghcr.io/sooperset/mcp-atlassian:latest" #image name
        ]
    )
    jira_workbench = McpWorkbench(jira_server_params)

    # playwright mcp server
    playwright_server_params = StdioServerParams(
        command="npx",
        args=["@playwright/mcp@latest"]
    )
    playwright_workbench = McpWorkbench(playwright_server_params)

    async with jira_workbench, playwright_workbench:
        bug_analyst = AssistantAgent(
            name="BugAnalyst",
            model_client=modal_client,
            workbench=jira_workbench,
            system_message=("""You are a Bug Analyst specializing in Jira defect analysis.
        Your task is as follows:
        Goal - - Your role is to analyze defects and create comprehensive test scenarios.
        1. Retrieve and review the most recent **5 bugs** from the **CreditCardBanking Project** (Project Key: `CRED`) in Jira.
        2. Carefully read their descriptions and identify **recurring issues or common patterns**.
        3. Based on these patterns, design a **detailed user flow** that exercises the core features of the application and can serve as a robust **smoke test scenario**.

        Be very specific in your smoke test design:
        - Provide clear, step-by-step manual testing instructions.
        - Include exact **URLs or page routes** to visit.
        - Describe **user actions** (clicks, form inputs, submissions).
        - Clearly state the **expected outcomes or validations** for each step.

        If you detect **zero bugs** in the recent Jira query, attempt to re-query or note it clearly.

        When your analysis and scenario preparation is complete:
        - Clearly output the final smoke testing steps.
        - Finally, write: **'HANDOFF TO AUTOMATION'** to signal completion of your analysis.

        Thank you for your thorough analysis.""")
        )

        automation_analyst = AssistantAgent(
            name="AutomationAgent",
            model_client=modal_client,
            workbench=playwright_workbench,
            system_message=("You are a Playwright automation expert. Take the user flow from BugAnalyst "
                            "and convert it into executable Playwright commands. Use Playwright MCP tools to  "
                            "execute the smoke test. Execute the automated test step by step and report "
                            "results clearly, including any errors or successes. Take screenshots at key "
                            "points to document the test execution."
                            "Make sure expected results in the bug are validated in your flow"
                            "Important : Use browser_wait_for to wait for success/error messages\n"
                            "   - Wait for buttons to change state (e.g., 'Applying...' to complete)\n"
                            "   - Verify expected outcomes as specified by BugAnalyst"
                            " Always follow the exact timing and waiting instructions provided"
                            "Complete ALL steps before saying 'TESTING COMPLETE, Execute each step fully, don't rush to completion"
                            )
        )

    team = RoundRobinGroupChat(
        participants=[bug_analyst, automation_analyst],

    )

    await Console(team.run_stream(task=))

asyncio.run(main())