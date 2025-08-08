"""
models.py

This file defines the Pydantic models used for structuring and validating the data extracted from the BOL.

The `ProductData` and `TransactionData` models are used to represent the product and transaction details that will be extracted from the uploaded document.
These models ensure that the extracted data follows a consistent structure and data types.

Key features:
- `ProductData`: Contains details about the product being transported (e.g., product code, name, octane rating, etc.).
- `TransactionData`: Contains details about the transaction (e.g., Bill of Lading number, card-in and card-out times, truck and trailer information, etc.).
"""


from pydantic import BaseModel, Field
from typing import List


class ProductData(BaseModel):
    product_code: str = Field(
        description="A unique identifier or code for the product, used for inventory tracking, transactions, and differentiating between various products. This code is often alphanumeric and follows a specific format to ensure consistency. ",
        example="P12345"  # Example of a unique product code.
    )
    product_name: str = Field(
        description="The name or designation of the product involved in the transaction. It represents the product being traded, sold, or transported, and helps in identifying the product within the system.  ",
        example="Premium Gasoline"  # Example of the product name.
    )
    octane_rating: str = Field(
        description="The octane rating of the product indicates its resistance to knocking or pinging during combustion. This number helps in determining the product’s suitability for specific engines and fuels.",
        example="95",  # Example of a product’s octane rating (common for gasoline).
    )
    temperature: str = Field(
        description="The temperature at which the product is stored, measured, or transported. This is an important parameter for products like fuels, chemicals, or gases where temperature can affect properties such as viscosity or volatility.",
        example="15",  # Example of temperature in degrees Celsius.
    )
    gravity: str = Field(
        description="The specific gravity of the product, which is the ratio of the product’s density to the density of water. This value helps in calculating the weight of the product for transportation, sales, and inventory purposes.",
        example="0.75",  # Example of specific gravity for a fuel product.
    )
    gross_gallons: str = Field(
        description="The total volume of the product before accounting for any losses, evaporation, or adjustments. This value represents the initial measurement and is essential for calculating costs and pricing.",
        example="1000",  # Example of gross gallons.
        alias="Total Gross" 
    )
    net_gallons: str = Field(
        description="The usable volume of the product after accounting for losses, evaporation, or other adjustments. This is the actual quantity available for sale or transport.",
        example="980",  # Example of net gallons after accounting for losses.
        alias="Total Net" 
    )

class TransactionData(BaseModel):
    bol_number: str = Field(
        description="The Bill of Lading (BOL) number is a unique identifier for a shipment. It acts as a contract between the shipper and the carrier, detailing the product being transported and the agreed terms. The BOL is crucial for verifying deliveries and ensuring proper documentation.Sometimes, this is also reprented as manifest or manifest number or BOL",
        example="0001481033",
        alias="BOL #" 
    )
    Card_in: str = Field(
        description="The time when the transaction started or the product was loaded onto the transport vehicle. It marks the start of the shipping or delivery cycle and helps in tracking the duration of the shipment. This should be recorded in a 24-hour time format. Sometimes, this is also represented as load in time, card in, load start, start time. just take out the hour and minute. not second. ",
        example="09:00",  # Example of card-in time (time only, no date).
        alias="Card In time" 
    )
    card_out: str = Field(
        description="The time when the product was delivered or the transaction was completed. It typically marks when the goods are offloaded from the transport vehicle, marking the end of the shipping cycle. This should be recorded in a 24-hour time format. Sometimes, this is also represented as load out time, card out, load end, end time.just take out the hour and minute. not second. ",
        example="17:00",  # Example of card-out time (time only, no date).
        alias="Card Out time" 
    )
    transaction_date: str = Field(
        description="The date on which either the card-in or card-out event occurs. This represents the key transactional date for the shipment, used as the reference date for tracking and delivery.  Sometimes, this is also represented as date, card in date, card out date",
        example="2025-08-01",  # Example of a transaction date (card-in or card-out).
        alias="Card In Date" 
    )
    carrier_name: str = Field(
        description="The name of the carrier company responsible for transporting the product. This is important for determining who is liable for the goods during transit and can help in resolving any issues that arise during transportation. Sometimes, this is also represented as Carrier or Loader",
        example="Global Logistics Inc.",  # Example of the carrier company name.
        alias="Carrier#/Loading#" 
    )
    supplier: str = Field(
        description="The name of the supplier who provides the product or goods being transported. This is the source or producer of the product and is essential for identifying the origin of the goods.",
        example="ABC Fuel Suppliers",  # Example of the supplier name.
        alias="Supplier#" 
    )
    driver_number: str = Field(
        description="A unique identifier for the driver responsible for transporting the product. This ID helps link the driver to the shipment for verification, monitoring, and accountability.",
        example="04210024",  # Example of a driver number.
        alias="Driver Number" 
    )
    product_data: List[ProductData] = Field(
        description="A list of products associated with the transaction. Each item in this list represents a specific product being transported in the shipment, including details like the product code, name, and quantity.",
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
        ]
    )
    truck_number: str = Field(
        description="The unique identification number assigned to the truck carrying the product. This number helps in tracking the vehicle during transit and matching it to the shipment documentation for verification purposes.",
        example="121",  # Example of truck identification number.
        alias="Truck Number" 
    )
    truck_license_no: str = Field(
        description="The license plate number of the truck carrying the product. This serves as a legal identifier for the vehicle, ensuring it is registered and permitted for the transportation of goods.",
        example="YCRG439",  # Example of truck license plate number.
        alias="Truck License Number" 
    )
    trailer_numbers: List[str] = Field(
        description="A list of trailer numbers associated with the shipment. These numbers identify the trailers attached to the truck and help track the goods throughout the transportation process.",
        example=["HU66720", "09560"],  # Example of trailer numbers.
        alias="Trailer Number" 
    )
    trailer_license_nos: List[str] = Field(
        description="A list of license plate numbers for the trailers. This information is important for tracking and verifying the specific trailers used during transport.",
        example=["YCRE912", "PCRO916"],  # Example trailer license plate numbers.
        alias="Trailer License Number" 
    )