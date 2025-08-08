from llama_cloud.types import ExtractConfig, ExtractMode

prompt = (
    "Please extract the following details from the document provided:\n"
    "- The **Bill of Lading (BOL) number**, which may also be referred to as 'manifest', 'Manifest Number', 'Consignment Number', 'Load Number'.\n"
    "- **Card-in time** (start of transaction/load) and **Card-out time** (end of transaction/delivery). These may also appear as 'Load Start Time', 'Load In Time', 'Load Out Time', 'End Time'. Just take out the hour and minute, not second\n"
    "- **Transaction date** (date of transaction), which may be written as 'Card In Date', 'Card Out Date', or simply 'Date'.\n"
    "- The **Carrier Name**, which may be referred to as 'carrier', 'Loader', 'Transporter', or 'Haulier'.\n"
    "- **Supplier Name**, which may be written as 'Vendor', 'Manufacturer', or 'Provider'.\n"
    "- **Driver number** or **Driver ID**, which could be written as 'Driver Identifier' or 'Transporter ID'.\n"
    "- **Truck Number** and **Truck License Plate Number**, which could also appear as 'Vehicle Number' or 'Plate Number'.\n"
    "- **Trailer Numbers** and **Trailer License Plate Numbers**. These could be represented as 'Trailer ID' or 'Vehicle ID'.\n"
    "- **Product details**, including product code, product name, octane rating (for fuel), specific gravity, gross and net gallons.\n"
    "- Ensure that all extracted data is formatted properly, particularly date and time fields (use 24-hour format), and numerical fields like gallons are accurate.\n"
    "- Be sure to provide all available details.\n"
)

# Define the extraction config globally
EXTRACTION_CONFIG = ExtractConfig(
    use_reasoning=True,
    cite_sources=True,
    extraction_mode=ExtractMode.MULTIMODAL,
    system_prompt=prompt
)
