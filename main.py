# main.py

import time
import json
import logging
import uuid
from llama_cloud_services import LlamaExtract
from pydantic import BaseModel, Field
from typing import List

# Set up logging
logging.basicConfig(
    filename="transaction_extraction.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# API key for LlamaCloud service
LLAMA_CLOUD_API_KEY = "llx-w6VoZes94aUPjiqemJdTgmg6J1XROS0EvXEOzoGbEt84K98M"

class ProductData(BaseModel):
    product_code: str = Field(
        description="Unique identifier or code for the product, used for inventory tracking and transactions.",
        example="QQQ009"  # Example product code
    )
    product_name: str = Field(
        description="The name or designation of the product being dealt with in the transaction.",
        example="Premium Gasoline"  # Example product name
    )
    octane_rating: str = Field(
        description="The octane rating of the product, which indicates its resistance to knocking or pinging during combustion.",
        example="95"  # Example octane rating
    )
    temperature: str = Field(
        description="The temperature at which the product is stored or measured.",
        example="15"  # Example temperature
    )
    gravity: str = Field(
        description="The specific gravity of the product, useful for determining its weight and volume.",
        example="0.75"  # Example specific gravity
    )
    gross_gallons: str = Field(
        description="The total volume of the product before accounting for losses or adjustments.",
        example="1000"  # Example gross gallons
    )
    net_gallons: str = Field(
        description="The usable volume of the product after accounting for adjustments.",
        example="980"  # Example net gallons
    )

class TransactionData(BaseModel):
    bol_number: str = Field(
        description="The Bill of Lading (BOL) number, which is a unique identifier for a shipment of goods.",
        example="0001481033"  # Example BOL number
    )
    card_in: str = Field(
        description="The date and time when the transaction was initiated or the product was loaded.",
        example="2025-08-01 09:00"  # Example card-in time
    )
    card_out: str = Field(
        description="The date and time when the product was delivered or the transaction was completed.",
        example="2025-08-01 17:00"  # Example card-out time
    )
    truck_number: str = Field(
        description="The identification number of the truck carrying the product.",
        example="121"  # Example truck number
    )
    truck_license_no: str = Field(
        description="The license plate number of the truck.",
        example="YCRG439"  # Example truck license plate
    )
    trailer_numbers: List[str] = Field(
        description="A list of trailer numbers associated with the shipment.",
        example=["HU66720", "09560"]  # Example trailer numbers
    )
    trailer_license_nos: List[str] = Field(
        description="A list of license plate numbers for the trailers.",
        example=["YCRE912", "PCRO916"]  # Example trailer license plates
    )
    driver_number: str = Field(
        description="A unique identifier for the driver responsible for transporting the product.",
        example="04210024"  # Example driver number
    )
    carrier_name: str = Field(
        description="The name of the carrier responsible for the transportation and delivery of the product from the supplier to the destination.",
        example="Global Logistics Inc."  # Example carrier name
    )
    supplier: str = Field(
        description="The name of the supplier who provides the product or goods being transported. The supplier is the source or producer of the product.",
        example="ABC Fuel Suppliers"  # Example supplier name
    )
    product_data: List[ProductData] = Field(
        description="A list of products associated with the transaction.",
        example=[
            {
                "product_code": "P12345",
                "product_name": "Premium Gasoline",
                "octane_rating": "95",
                "temperature": "15",
                "gravity": "0.75",
                "gross_gallons": "1000",
                "net_gallons": "980"
            },
            {
                "product_code": "P67890",
                "product_name": "Diesel Fuel",
                "octane_rating": "N/A",
                "temperature": "18",
                "gravity": "0.85",
                "gross_gallons": "500",
                "net_gallons": "490"
            }
        ]  # Example product data
    )

def extract_transaction_data(file_path: str, api_key: str = LLAMA_CLOUD_API_KEY) -> dict:
    try:
        logging.info(f"Extracting data from file: {file_path}")
        
        # Initialize LlamaExtract client with API key
        extractor = LlamaExtract(api_key=api_key)
        
        # Create a unique agent name using UUID and timestamp
        unique_agent_name = f"transaction-parser-{uuid.uuid4().hex}-{int(time.time())}"
        
        # Create agent with MULTIMODAL mode, system prompt, and high_resolution_mode
        agent = extractor.create_agent(
            name=unique_agent_name,
            data_schema=TransactionData
            # config={
            #     "system_prompt": "Focus on extracting accurate transaction data from the BOL document."
 
            # }
        )
        
        # Perform extraction
        result = agent.extract(file_path)
        
        # Log and return extracted data
        logging.info(f"File: {file_path} - Extracted Data: {json.dumps(result.data, indent=4)}")
        return result.data
    except Exception as e:
        logging.error(f"Error during extraction for {file_path}: {str(e)}")
        raise
