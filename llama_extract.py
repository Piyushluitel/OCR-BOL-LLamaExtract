"""
llama_extract.py

This file contains functions to interact with LlamaExtract, specifically to create or reuse extraction agents.

The agent handles the extraction of structured transaction data from uploaded documents. The existing agent is reused whenever possible to ensure efficiency and consistency in the extraction process.

Key features:
- `get_existing_agent`: Retrieves the existing LlamaExtract agent by name.
- Reuses the agent instead of creating a new one, ensuring faster execution and avoiding duplicate agent creation.
"""


from llama_cloud_services import LlamaExtract
from config import EXTRACTION_CONFIG

# Global variable to store the agent
existing_agent = None

def get_existing_agent(api_key: str):
    global existing_agent
    if existing_agent is None:
        # Reuse the existing agent with the name "OCR_BOL_FLEETPANDA"
        unique_agent_name = "OCR_BOL_FLEETPANDA"
        
        # Initialize the LlamaExtract client
        extractor = LlamaExtract(api_key=api_key)
        
        # Get the existing agent by name
        existing_agent = extractor.get_agent(unique_agent_name)
        
        print(f"Reusing the existing agent '{unique_agent_name}'.")

        # Apply the configuration to the existing agent
        existing_agent.config = EXTRACTION_CONFIG  # Reapply the saved config to the existing agent
    
    return existing_agent
