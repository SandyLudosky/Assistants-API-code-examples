import openai
from dotenv import load_dotenv
from utils import retrieve_annotations, save_file

load_dotenv()

LANGUAGE_MODEL = "gpt-3.5-turbo-1106"
LANGUAGE_MODEL_GPT_4 = "gpt-4-1106-preview"
ASSISTANT_NAME = "Senior Python Developer"
ASSISTANT_DEFAULT_INSTRUCTIONS = """You are a Senior Python Developer.
    Write, run and print code to answer math questions.
    You are also knowledgeable about tech related topics."""

# Initialize clients with API keys
client = openai.OpenAI()


def print_messages_from_thread(thread_id):
    """Prints all messages from a thread."""
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for message in messages:
        if message.role == "assistant":
            print(message)
            print(f"{message.role}: {message.content[0].text.value}")

        # check for annotations to process files


def create_assistant():
    """Creates an assistant with the default instructions."""
    assistant = client.beta.assistants.create(
        name=ASSISTANT_NAME,
        instructions=ASSISTANT_DEFAULT_INSTRUCTIONS,
        tools=[{"type": "code_interpreter"}],
        model=LANGUAGE_MODEL,
    )
    print(f"new assistant created, id#: {assistant.id} \n")
    return assistant


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
        if run.status in ["completed", "in progress"]:
            return run


def main():
    # Step 1 : Add the file to the assistant
    assistant = create_assistant()
    # Step 2 - Create a Thread
    thread = create_thread()

    print(
        """Hello, I am a Senior Developer. Just ask me if you need help \n (type 'exit' to quit)"""
    )

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Step 3 - Add a message to the thread
        add_message_to_thread(thread, user_input)

        # Step 4 - Run the Assistant
        run = run_assistant(thread, assistant)

        # Step 5 - Check the run status
        run = check_status(thread.id, run.id)

        if run.status == "failed":
            print(run.error)
            continue

        # Step 6 - Pring the messages from the thread
        print_messages_from_thread(thread.id)


if __name__ == "__main__":
    main()
