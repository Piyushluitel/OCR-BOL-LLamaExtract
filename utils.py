from llama_extract import get_existing_agent

LLAMA_CLOUD_API_KEY = "llx-w6VoZes94aUPjiqemJdTgmg6J1XROS0EvXEOzoGbEt84K98M"

def extract_transaction_data(file_path: str, api_key: str) -> dict:
    # Get the agent (will reuse the existing one)
    agent = get_existing_agent(api_key)
    
    # Now use this agent for extraction
    result = agent.extract(file_path)
    return result.data
