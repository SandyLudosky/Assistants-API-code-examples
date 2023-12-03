### This Gist demos how to use the latest OpenAI Assistants API with Internet access
# Step 1: Upgrade to Python SDK v1.2 with pip install --upgrade openai
# Step 2: Install Tavily Python SDK with pip install tavily-python
# Step 3: Build an OpenAI assistant with Python SDK documentation - https://platform.openai.com/docs/assistants/overview

import os
import json
import openai
from dotenv import load_dotenv
from colorama import Fore, Style
from tavily import TavilyClient
from functions import get_current_weather

load_dotenv()


# Specify the path to your JSON file
json_file_path = "functions.json"

# Open the JSON file and load its content
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)


# Initialize clients with API keys
client = openai.OpenAI()

LANGUAGE_MODEL = "gpt-3.5-turbo-1106"
LANGUAGE_MODEL_GPT_4 = "gpt-4-1106-preview"
ASSISTANT_NAME = "Alex, Weather Report"
ASSISTANT_DEFAULT_INSTRUCTIONS = """
You are a news and weather expert.
"""
TOOLS = [data["weather"]]

# topics about finance : https://www.sunlife.ca/en/tools-and-resources/money-and-finances/investing-basics/the-12-top-personal-finance-topics-of-2022/#5


def retrieve_messages_from_thread(thread_id):
    """Prints all messages from a thread."""
    return client.beta.threads.messages.list(thread_id=thread_id)


def print_messages_from_thread(messages):
    """Prints all messages from a thread."""
    messages = [message for message in messages if message.role == "assistant"]
    for message in messages:
        print(
            Fore.CYAN
            + f"Agent: {message.content[0].text.value}"
            + Fore.RESET
            + Style.RESET_ALL
        )


def create_assistant():
    """Creates an assistant with the default instructions."""
    assistant = client.beta.assistants.create(
        instructions=ASSISTANT_DEFAULT_INSTRUCTIONS,
        model=LANGUAGE_MODEL,
        tools=[{"type": "retrieval"}],
    )
    print(f"new assistant created, id#: {assistant.id} \n")
    return assistant


def upload_file(file_name):
    return client.files.create(
        file=open(f"files/{file_name}", "rb"), purpose="assistants"
    )


def create_thread():
    """Creates a thread."""
    return client.beta.threads.create()


def add_message_to_thread(thread, message):
    """Adds a message to a thread."""
    return client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message,
    )


def run_assistant(thread, assistant):
    """Runs an assistant on a thread."""
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=ASSISTANT_DEFAULT_INSTRUCTIONS,
    )
    print(f"Run ID: {run.id}")
    return run


def check_status(thread_id, run_id):
    """Checks the status of a run every second until it is completed."""
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        print(f"Current run status: {run.status}")
        if run.status in ["completed", "in progress", "requires_action"]:
            return run


# Function to handle tool output submission
def submit_tool_outputs(thread, run):
    tools_to_call = run.required_action.submit_tool_outputs.tool_calls
    tool_output_array = []

    for tool in tools_to_call:
        output = None

        if tool.function.name == "weather":
            location = json.loads(tool.function.arguments)["location"]
            unit = json.loads(tool.function.arguments)["unit"]
            output = get_current_weather(location, unit)
            tool_output_array.append({"tool_call_id": tool.id, "output": output})

    return tool_output_array


def submit_functions_output(thread, run, tool_outputs):
    return client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
    )


def create_assistant():
    # Create an assistant
    assistant = client.beta.assistants.create(
        instructions=ASSISTANT_DEFAULT_INSTRUCTIONS,
        model=LANGUAGE_MODEL,
        tools=TOOLS,
    )
    print(f"Assistant ID: {assistant.id}")
    return assistant


def call_assistant(user_input):
    # Step 1 - Create an assistant
    assistant = create_assistant()

    # Step 2 - create a thread
    thread = create_thread()

    print(Fore.CYAN + """Agent: Hello, H\n (type 'exit' to quit)""" + Fore.RESET)

    while True:
        # Step 3 - Add a message to the thread
        add_message_to_thread(thread, user_input)

        # Step 4 - Initiate a run
        run = run_assistant(thread, assistant)

        # Step 5 - Check the run status
        run = check_status(thread.id, run.id)

        if run.status == "failed":
            print(run.error)
            continue

        # Check if run status "requires_action"
        elif run.status == "requires_action":
            tool_outputs = submit_tool_outputs(thread, run)
            submit_functions_output(thread, run, tool_outputs)
            run = check_status(thread.id, run.id)

        # Step 6 - Pring the messages from the thread if the run is completed
        if run.status == "completed":
            messages = retrieve_messages_from_thread(thread.id)
            print_messages_from_thread(messages)

        # Print messages from the thread
        return messages
