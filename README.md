# Pantry MCP Orchestrator

```mermaid
flowchart LR
    U[User runs\npython main.py] -->|starts| A[MCPApp\n(dinner_party_orchestrator)]
    A -->|uses| O[Orchestrator\n(plan_type=full)]
    O -->|calls| AR1[Agent: pantry_reader]
    O -->|calls| AR2[Agent: menu_planner]
    O -->|calls| AR3[Agent: shopping_list_writer]

    O -->|LLM calls via\nAugmented LLM| LLM[(LLM\nOpenAI gpt-4o)]

    subgraph MCP Servers
      FS[filesystem MCP server\n(mcp-server-filesystem)]
    end

    AR1 -->|read pantry files| FS
    AR2 -->|read pantry summary\nwrite intermediate info| FS
    AR3 -->|write outputs| FS

    subgraph Local Files
      TASK[task.md]
      PLAN[plan.md]
      PANTRY[pantry/pantry.txt]
      OUTPUT[output/\ndinner_plan.md\nshopping_list.md]
    end

    A -->|reads| TASK
    O -->|writes| PLAN
    FS -->|reads| PANTRY
    FS -->|writes| OUTPUT

### **Sequence Diagram**
```md
```mermaid
sequenceDiagram
    participant User
    participant main.py
    participant Orchestrator
    participant pantry_reader
    participant menu_planner
    participant shopping_list_writer
    participant FS as filesystem MCP
    participant LLM

    User->>main.py: run python main.py
    main.py->>FS: start filesystem server
    main.py->>main.py: read task.md
    main.py->>Orchestrator: instantiate orchestrator

    Orchestrator->>LLM: generate plan
    LLM-->>Orchestrator: list of steps

    Orchestrator->>pantry_reader: read pantry
    pantry_reader->>FS: list pantry files
    pantry_reader->>FS: read pantry.txt
    FS-->>pantry_reader: contents
    pantry_reader->>LLM: generate summary
    LLM-->>pantry_reader: structured pantry data

    Orchestrator->>menu_planner: propose 3 menus
    menu_planner->>LLM: generate menus + missing ingredients
    LLM-->>menu_planner: menu options

    Orchestrator->>shopping_list_writer: produce output files
    shopping_list_writer->>LLM: generate markdown
    shopping_list_writer->>FS: write output/dinner_plan.md
    shopping_list_writer->>FS: write output/shopping_list.md

    Orchestrator-->>main.py: task complete
    main.py-->>User: finished
