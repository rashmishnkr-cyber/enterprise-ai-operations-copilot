import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.knowledge_tool import ask_question
from tools.sql_tool import run_sql


load_dotenv()

client = OpenAI()


# --------------------------------------------------
# Tool Definitions
# --------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "name": "knowledge_tool",
        "description": (
            "Search company documents and answer questions using "
            "the enterprise knowledge base. Use this for company "
            "policies, definitions, SOPs, manuals, procedures, "
            "and documentation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The user's question."
                }
            },
            "required": ["question"],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "sql_tool",
        "description": (
            "Query the Logistics Analytics SQL Server database. "
            "Use this for shipment metrics, carrier performance, "
            "counts, reports, analytics, and numerical business data."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The user's business analytics question."
                }
            },
            "required": ["question"],
            "additionalProperties": False
        }
    }
]


# --------------------------------------------------
# Execute Tools
# --------------------------------------------------

def execute_tool(tool_name, arguments):

    if tool_name == "knowledge_tool":

        return ask_question(
            arguments["question"]
        )

    if tool_name == "sql_tool":

        return run_sql(
            arguments["question"]
        )

    return f"Unknown tool: {tool_name}"


# --------------------------------------------------
# Agent
# --------------------------------------------------

def agent(question):

    conversation = [
        {
            "role": "user",
            "content": question
        }
    ]

    while True:

        response = client.responses.create(
            model="gpt-4.1",

            instructions="""
You are an enterprise AI operations assistant.

Your job is to completely answer the user's question.

You have two tools.

KNOWLEDGE TOOL:
Use this for company-specific information:
- Policies
- SOPs
- Manuals
- Procedures
- Definitions
- Documentation

SQL TOOL:
Use this for operational information:
- Shipment metrics
- Carrier performance
- Counts
- Reports
- Analytics
- Numerical business questions

IMPORTANT RULES:

1. Read the ENTIRE user question before deciding what to do.

2. If the question contains multiple requests, answer EVERY part.

3. You may call multiple tools during the same conversation.

4. If one tool answers only part of the question,
   continue and call another tool when necessary.

5. Do not stop after answering only one part of a multi-part question.

6. You may answer directly when general knowledge is sufficient
   and company-specific information is not required.

7. Never invent company policies or operational data.

8. After all required tools have been used, provide one
   clear, complete answer addressing every part of the
   original question.
""",

            tools=TOOLS,

            input=conversation
        )

        # Find tool calls
        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # No tool calls means GPT believes it can answer
        if not tool_calls:

            return response.output_text

        # Preserve GPT's response
        conversation.extend(response.output)

        # Execute ALL requested tools
        for tool_call in tool_calls:

            arguments = json.loads(
                tool_call.arguments
            )

            print(
                f"Calling tool: {tool_call.name}"
            )

            result = execute_tool(
                tool_call.name,
                arguments
            )

            conversation.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(result)
                }
            )


# --------------------------------------------------
# Local Test
# --------------------------------------------------

if __name__ == "__main__":

    question = (
        "What is Python?"
    )
    answer = agent(question)
    
    print("\n-----------------------------")
    print("FINAL ANSWER")
    print("-----------------------------")
    print(answer)