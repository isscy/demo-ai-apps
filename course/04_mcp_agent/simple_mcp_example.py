import os
from dotenv import load_dotenv
from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands.tools import http_request

# Load environment variables
load_dotenv()

# Validate API key
nebius_api_key = os.getenv("NEBIUS_API_KEY")
if not nebius_api_key:
    raise ValueError("NEBIUS_API_KEY environment variable is required")

# Configure the language model
model = LiteLLMModel(
    client_args={"api_key": nebius_api_key},
    model_id="nebius/deepseek-ai/DeepSeek-V3-0324",
)

# Create a simple agent with HTTP request tool
agent = Agent(
    model=model,
    tools=[http_request],
    system_prompt=("You are a helpful assistant that can make HTTP requests. "
                  "Use the http_request tool to get information from APIs.")
)

# Example query that doesn't require external MCP servers
user_query = "Get the current time from worldtimeapi.org for Beijing"
print(f"User Query: {user_query}")

# Execute the query
response = agent(user_query)

print("\nAgent Response:")
print(response)
