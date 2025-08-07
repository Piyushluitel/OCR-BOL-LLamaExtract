from llama_cloud.types import ExtractConfig, ExtractMode

# Define the extraction config globally
EXTRACTION_CONFIG = ExtractConfig(
    use_reasoning=True,
    cite_sources=True,
    extraction_mode=ExtractMode.MULTIMODAL,
    system_prompt="Please extract the transactional details first, including the Bill of Lading number, transaction start and completion times, truck identification and license plate, trailer numbers and license plates, driver’s unique ID, carrier name, and supplier’s name. Once the transaction data is extracted, proceed to extract the product-specific details, including the unique identifier for each product, its name, octane rating, storage or measured temperature, specific gravity, total volume before adjustments, and usable volume after adjustments. Ensure that all extracted data follows the required format, particularly for date-time and numerical fields like gallons. Handle missing or null values appropriately and ensure consistency and accuracy in the extraction process. Pay special attention to the correct extraction of product-related information, including details such as the octane rating for fuel products. Maintain consistency in time formats (using 24-hour format) and ensure that numerical fields like gross and net gallons are extracted accurately. Return the data in the specified structured format, ensuring accuracy across all fields."
)
