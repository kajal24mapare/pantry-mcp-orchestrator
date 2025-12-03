# Pantry MCP Orchestrator

+--------------------------------------------------------------+
|                    Pantry MCP Orchestrator                   |
|                      (python main.py)                        |
+------------------------------+-------------------------------+
                               |
                               v
                    +------------------------+
                    |        MCPApp          |
                    |  dinner_party_...      |
                    +-----------+------------+
                                |
                                v
                       +-----------------+
                       |  Orchestrator   |
                       | (mcp-agent)     |
                       +--------+--------+
                                |
              +-----------------+------------------+
              |                 |                  |
              v                 v                  v
   +----------------+  +----------------+  +------------------------+
   |  Agent         |  |  Agent         |  |  Agent                 |
   | pantry_reader  |  | menu_planner   |  | shopping_list_writer   |
   +--------+-------+  +--------+-------+  +-----------+-----------+
            |                   |                      |
            |                   |                      |
            v                   v                      v
   +----------------------------------------------------------+
   |              filesystem MCP server (mcp-server-filesystem)|
   +-----------------------------+----------------------------+
                                 |
                                 v
                        Local project directory
                                 |
     +----------------+----------+-----------------------------+
     |                |          |                             |
     v                v          v                             v
+---------+     +----------+  +----------------+     +----------------------+
| task.md |     | plan.md  |  | pantry/        |     | output/              |
|         |     | (auto)   |  |   pantry.txt   |     |  dinner_plan.md      |
|         |     |          |  |   ...          |     |  shopping_list.md    |
+---------+     +----------+  +----------------+     +----------------------+

   Orchestrator:
   - Reads task.md
   - Coordinates agents
   - Writes plan.md

   Agents:
   - Use filesystem MCP to read/write files as needed.


------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------

User
 |
 |  run: python main.py
 v
main.py
 |
 |-- load mcp_agent.config.yaml
 |-- start MCPApp (dinner_party_orchestrator)
 |-- ensure filesystem MCP server sees current directory
 |-- read task.md
 |-- create Orchestrator with 3 agents
 v
Orchestrator
 |
 |-- ask LLM to create a plan (multi-step)
 |   (decide order: pantry_reader -> menu_planner -> shopping_list_writer)
 |
 |--------------------------------------------------------+
 |                                                        |
 v                                                        v
Agent: pantry_reader                              Agent: menu_planner
 |                                                        ^
 |-- via filesystem MCP:                                  |
 |      list/read pantry/pantry.txt                       |
 |-- summarize ingredients using LLM                      |
 |-- return structured pantry summary                     |
 +--------------------------------------------------------+
 |
 v
Orchestrator
 |
 |-- give pantry summary + task to menu_planner
 v
Agent: menu_planner
 |
 |-- use LLM to propose 3 menus (starter, main, dessert)
 |-- mark which ingredients are available vs missing
 |-- return menus + pros/cons
 |
 v
Orchestrator
 |
 |-- decide which menu is “best” (based on instructions)
 |-- send chosen menu + context to shopping_list_writer
 v
Agent: shopping_list_writer
 |
 |-- use LLM to generate:
 |      - dinner_plan.md (friendly explanation)
 |      - shopping_list.md (grouped list)
 |-- via filesystem MCP:
 |      write output/dinner_plan.md
 |      write output/shopping_list.md
 |
 v
Orchestrator
 |
 |-- return final status/result to main.py
 v
main.py
 |
 |-- print "done" / logging info
 v
User
 |
 |-- opens files in output/ to see plan & shopping list
 v
(End)
