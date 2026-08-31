import json
import os

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set in the environment variables."
    )


# ============================================================
# 2. Initialize Groq client
# ============================================================

client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-120b"


# ============================================================
# 3. Our actual Python function
# ============================================================

def get_user(user_id: int) -> dict:
    """
    Get user information.

    In a real application this could query:
    - MongoDB
    - PostgreSQL
    - REST API
    - Redis
    """

    users = {
        1: {
            "id": 1,
            "name": "Chandan Rout",
            "role": "Full Stack Developer",
            "experience": 6,
            "skills": [
                "React",
                "Node.js",
                "TypeScript",
                "Python",
                "FastAPI",
            ],
        },
        2: {
            "id": 2,
            "name": "Rahul Sharma",
            "role": "Backend Developer",
            "experience": 4,
            "skills": [
                "Python",
                "FastAPI",
                "PostgreSQL",
            ],
        },
    }

    user = users.get(user_id)

    if not user:
        return {
            "error": f"User with ID {user_id} was not found."
        }

    return user


# ============================================================
# 4. Tell the LLM about our function
# ============================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_user",
            "description": (
                "Get user information using the user's numeric ID. "
                "Use this function when the user asks about a user's "
                "name, role, experience, or skills."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The numeric ID of the user.",
                    }
                },
                "required": ["user_id"],
            },
        },
    }
]


# ============================================================
# 5. Map tool names to actual Python functions
# ============================================================

available_functions = {
    "get_user": get_user,
}


# ============================================================
# 6. Execute a tool call
# ============================================================

def execute_tool_call(tool_call):
    function_name = tool_call.function.name

    if function_name not in available_functions:
        raise ValueError(
            f"Unknown function: {function_name}"
        )

    function_to_call = available_functions[function_name]

    function_args = json.loads(
        tool_call.function.arguments
    )

    print("\n--- TOOL CALL ---")
    print("Function:", function_name)
    print("Arguments:", function_args)

    result = function_to_call(**function_args)

    print("Result:", result)
    print("-----------------\n")

    return result


# ============================================================
# 7. Run conversation
# ============================================================

def run_conversation(user_prompt: str):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful user information assistant. "
                "Use the get_user tool whenever you need user "
                "information. Do not invent user information."
            ),
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    # --------------------------------------------------------
    # First request
    # --------------------------------------------------------

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message

    # --------------------------------------------------------
    # Check if model wants to call a function
    # --------------------------------------------------------

    if response_message.tool_calls:

        # Add assistant's tool-call message to conversation
        messages.append(response_message)

        # ----------------------------------------------------
        # Execute every requested tool
        # ----------------------------------------------------

        for tool_call in response_message.tool_calls:

            function_result = execute_tool_call(
                tool_call
            )

            # ------------------------------------------------
            # Send tool result back to the LLM
            # ------------------------------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": json.dumps(function_result),
                }
            )

        # ----------------------------------------------------
        # Ask LLM for final answer
        # ----------------------------------------------------

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )

        return final_response.choices[0].message.content

    # --------------------------------------------------------
    # Model didn't use a tool
    # --------------------------------------------------------

    return response_message.content


# ============================================================
# 8. Run the application
# ============================================================

if __name__ == "__main__":

    question = "What is Chandan's role and how many years of experience does he have?"

    answer = run_conversation(question)

    print("\n==============================")
    print("FINAL ANSWER")
    print("==============================")
    print(answer)