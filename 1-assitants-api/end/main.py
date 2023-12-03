import openai
from colorama import Fore
from dotenv import load_dotenv


load_dotenv()

# Initialize clients with API keys
client = openai.OpenAI()

DEFAULT_USER_MESSAGE = "I need to solve the equation `3x + 11 = 14`. Can you help me?"


def main():
    print("Welcome to the Math Homework Assistant! (Type 'x' to exit)")
    messages = []

    # Step1 - Create the Assistant
    assistant = client.beta.assistants.create(
        name="Math Homework Helper",
        instructions="You are an experienced Math Mentor and also knowlegeable in Physics and Chemistry. ",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo-1106",
    )

    # Step 2 - Create the Thread
    thread = client.beta.threads.create()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "x":
            print("Goodbye!")
            break

        # Step 3 - Add a message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_input
        )

        # Step 4 - Run the Assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="You are an experienced Math Mentor and also knowlegeable in Physics and Chemistry. ",
        )

        # Step 5 - Check the Run Status (until it is completed)

        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Current run status: {run.status}")

            # Step 6 - Display the Assistant's response
            if run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                messages = [
                    message for message in messages if message.role == "assistant"
                ]
                break

        print(Fore.CYAN + f"Agent: {messages[0].content[0].text.value}" + Fore.RESET)


if __name__ == "__main__":
    main()
