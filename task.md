# Dinner Party Planner Task

You are an orchestrator that coordinates several specialist agents using tools
exposed by MCP servers.

Goal:
Plan a dinner party for 4 guests based on what is available in the local pantry.

Requirements:

1. Use the filesystem MCP server to:
   - Inspect the `pantry/` directory.
   - Read any files there (especially `pantry.txt`) to understand which 
     ingredients and approximate quantities are available.

2. Based on the pantry contents, propose **three distinct dinner menus**.
   For each menu:
   - Include a starter, main course, and dessert.
   - Briefly describe each dish.
   - Note which ingredients are already available and which are missing.

3. Choose the single best menu for the dinner party, preferring options that:
   - Use more existing pantry ingredients.
   - Are reasonably simple to cook for a home cook.
   - Fit a casual, fun dinner with friends.

4. Produce the following files via the filesystem server:

   - `output/dinner_plan.md`
     - A friendly explanation of the chosen menu.
     - Includes the three menu options considered with reasoning for 
       why the final one was chosen.
     - Includes rough timing (prep/cook) for each course.

   - `output/shopping_list.md`
     - A shopping list of missing ingredients for the chosen menu.
     - Group items by category (e.g. Vegetables, Dairy, Pantry, Other).
     - Include approximate quantities where possible.

5. Be explicit when using tools. Make sure tool calls are grounded in files
   that actually exist, and avoid hallucinating paths or filenames.
