import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""

    # Get API key from environment variable
    groq_api_key = os.getenv(
        "GROQ_API_KEY", "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")

    # Config file path - change this to your config file
    config_file = "./gym.json"

    print("Initializing chat...")

    try:
        # Create MCP client and agent with memory enabled
        client = MCPClient.from_config_file(config_file)
        llm = ChatGroq(
            model="qwen-qwq-32b",
            api_key=groq_api_key
        )

        # Create agent with memory enabled
        agent = MCPAgent(
            llm=llm,
            client=client,
            max_steps=15,
            memory_enabled=True  # Enable built-in conversation memory
        )

        print("\n===== Interactive MCP Chat =====")
        print("Type 'exit' or 'quit' to end the conversation")
        print("Type 'clear' to clear conversation history")
        print("==================================\n")

        # Main chat loop
        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Check for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    except Exception as e:
        print(f"Error initializing chat: {e}")
    finally:
        # Clean up
        if 'client' in locals() and client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_memory_chat())
