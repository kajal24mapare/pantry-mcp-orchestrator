# main.py

import asyncio
import os
import time
from pathlib import Path

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator
from rich import print


app = MCPApp(name="dinner_party_orchestrator")


async def example_usage() -> None:
    # Boot the MCPApp runtime (loads config, connects MCP servers, etc.)
    async with app.run() as dinner_app:
        logger = dinner_app.logger
        context = dinner_app.context

        # Make sure the filesystem MCP server can see the current project directory
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])

        # --- Define Agents ---

        # 1) Pantry Reader
        pantry_reader = Agent(
            name="pantry_reader",
            instruction=(
                "You are a meticulous pantry analyst.\n"
                "Use the filesystem MCP server to inspect the `pantry/` directory.\n"
                "Read files like `pantry.txt` and produce a clear, structured summary\n"
                "of available ingredients and quantities. If quantities are not\n"
                "specified, assume 1-2 servings worth by default.\n\n"
                "Return your findings as:\n"
                "- A bullet list of ingredients\n"
                "- Optional notes about freshness or typical uses\n"
            ),
            server_names=["filesystem"],
        )

        # 2) Menu Planner
        menu_planner = Agent(
            name="menu_planner",
            instruction=(
                "You are a creative dinner menu planner.\n"
                "Based on the pantry summary and the dinner party requirements,\n"
                "propose THREE distinct menus for 4 guests.\n"
                "Each menu must include:\n"
                "- Starter\n"
                "- Main course\n"
                "- Dessert\n\n"
                "For each dish, briefly describe it and list which ingredients are:\n"
                "- Already available in the pantry\n"
                "- Missing and need to be bought\n\n"
                "At the end, provide a short comparison of the three menus with pros/cons.\n"
            ),
            server_names=["filesystem"],
        )

        # 3) Shopping List Writer
        shopping_list_writer = Agent(
            name="shopping_list_writer",
            instruction=(
                "You are a practical kitchen assistant.\n"
                "Given the chosen menu and pantry contents, your job is to:\n"
                "1. Generate a friendly dinner plan in Markdown and write it to\n"
                "   `output/dinner_plan.md` via the filesystem MCP server.\n"
                "   - Explain the three menus that were considered.\n"
                "   - Justify which one was chosen for the party.\n"
                "   - Include estimated prep and cook times for each course.\n"
                "2. Generate a shopping list in Markdown and write it to\n"
                "   `output/shopping_list.md`.\n"
                "   - Group items by category (Vegetables, Dairy, Pantry, Other).\n"
                "   - Include approximate quantities.\n"
                "   - Avoid listing ingredients that are clearly already available.\n"
                "Make sure you actually use filesystem tools and create the files.\n"
            ),
            server_names=["filesystem"],
        )

        # --- Read the high-level task description ---
        task_path = Path("task.md")
        with open(task_path, "r", encoding="utf-8") as f:
            task = f.read()

        # --- Create Orchestrator with all agents ---
        orchestrator = Orchestrator(
            llm_factory=OpenAIAugmentedLLM,
            available_agents=[
                pantry_reader,
                menu_planner,
                shopping_list_writer,
            ],
            plan_type="full",
            plan_output_path=Path("plan.md"),
            max_iterations=6,
        )

        logger.info("Starting dinner party planning task...")

        # Execute the orchestrated workflow
        result = await orchestrator.generate_str(
            message=task,
            request_params=RequestParams(
                model="gpt-4o",
                maxTokens=8192,  # adjust if your provider uses a different field
            ),
        )

        logger.info(f"Dinner party planning task completed: {result}")


if __name__ == "__main__":
    start = time.time()
    asyncio.run(example_usage())
    end = time.time()
    print(f"[bold green]Total orchestration time:[/bold green] {end - start:.2f}s")