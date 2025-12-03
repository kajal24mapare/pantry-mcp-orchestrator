# Pantry MCP Orchestrator

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
    AR2 -->|read pantry summary,\nwrite temp files if needed| FS
    AR3 -->|write outputs| FS

    subgraph Local Files
      TASK[task.md]
      PLAN[plan.md\n(generated)]
      PANTRY[pantry/\npantry.txt]
      OUTPUT[output/\n dinner_plan.md\n shopping_list.md]
    end

    A -->|reads| TASK
    O -->|writes plan| PLAN
    FS -->|reads| PANTRY
    FS -->|writes| OUTPUT

sequenceDiagram
    participant User
    participant main.py
    participant Orchestrator
    participant pantry_reader
    participant menu_planner
    participant shopping_list_writer
    participant FS as filesystem MCP
    participant LLM

    User->>main.py: python main.py
    main.py->>main.py: load mcp_agent.config.yaml
    main.py->>FS: start filesystem MCP (uvx mcp-server-filesystem)
    main.py->>main.py: read task.md
    main.py->>Orchestrator: create with 3 agents

    Orchestrator->>LLM: plan steps for task
    LLM-->>Orchestrator: plan (use pantry_reader, menu_planner, writer)

    Orchestrator->>pantry_reader: execute subtask
    pantry_reader->>FS: read pantry/pantry.txt
    FS-->>pantry_reader: pantry contents
    pantry_reader->>LLM: summarize pantry
    LLM-->>pantry_reader: structured pantry summary

    Orchestrator->>menu_planner: execute subtask
    menu_planner->>FS: read pantry summary / task
    menu_planner->>LLM: propose 3 menus + pros/cons
    LLM-->>menu_planner: menus, missing ingredients

    Orchestrator->>shopping_list_writer: execute subtask
    shopping_list_writer->>LLM: draft dinner_plan + shopping list
    LLM-->>shopping_list_writer: markdown content
    shopping_list_writer->>FS: write output/dinner_plan.md
    shopping_list_writer->>FS: write output/shopping_list.md

    Orchestrator-->>main.py: final result text
    main.py-->>User: done + files on disk
