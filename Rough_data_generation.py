import pandas as pd
import random
from datetime import datetime, timedelta

# Constants for random choices
PRODUCT_NAMES = ['Widget A', 'Widget B', 'Widget C', 'Widget D', 'Widget E']
CATEGORIES = ['Electronics', 'Clothing', 'Books', 'Furniture', 'Toys']
PAYMENT_TYPES = ['Credit Card', 'PayPal', 'Bank Transfer', 'Gift Card']
COUNTRIES = ['USA', 'Canada', 'UK', 'Germany', 'France']
SITES = ['Amazon', 'eBay', 'Flipkart', 'Walmart', 'Shopify']
PAYMENT_STATUS = ['Y', 'N']
FAILURE_REASONS = ['Insufficient Funds', 'Card Expired', 'Payment Gateway Error', 'Fraudulent Activity']

# Manually defined UUID-like strings
UUID_LIST = [
    '123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174001',
    '123e4567-e89b-12d3-a456-426614174002', '123e4567-e89b-12d3-a456-426614174003',
    '123e4567-e89b-12d3-a456-426614174004', '123e4567-e89b-12d3-a456-426614174005',
    '123e4567-e89b-12d3-a456-426614174006', '123e4567-e89b-12d3-a456-426614174007',
    '123e4567-e89b-12d3-a456-426614174008', '123e4567-e89b-12d3-a456-426614174009'
] * 10  # Repeat to have at least 100 UUIDs

# Correctly ordered columns
COLUMNS = [
    'Order_Id', 'Customer_Id', 'Customer_Name', 'Product_Id', 'Product_Name',
    'Product_Category', 'Payment_Type', 'Quantity_ordered', 'Price',
    'Date_and_Time_When_Order_Was_Placed', 'Customer_Country', 'Customer_City',
    'Site_From_Where_Order_Was_Placed', 'Payment_Transaction_Confirmation_Id',
    'Payment_Success_or_Failure', 'Payment_Failure_Reason'
]

def generate_record(index: int) -> dict:
    """Generate a single order record with a mix of valid and invalid data based on index."""
    record = {
        'Order_Id': UUID_LIST[index] if index % 10 != 0 else 'InvalidUUID',  # Invalid UUID every 10th record
        'Customer_Id': UUID_LIST[index] if index % 10 != 1 else 'InvalidCustomerId',  # Invalid Customer Id every 10th + 1 record
        'Customer_Name': f'Customer_{index}',
        'Product_Id': UUID_LIST[index] if index % 10 != 2 else 'InvalidProductId',  # Invalid Product Id every 10th + 2 record
        'Product_Name': random.choice(PRODUCT_NAMES),
        'Product_Category': random.choice(CATEGORIES) if index % 10 != 3 else 'InvalidCategory',  # Invalid Category every 10th + 3 record
        'Payment_Type': random.choice(PAYMENT_TYPES),
        'Quantity_ordered': random.randint(1, 5) if index % 10 != 4 else -1,  # Invalid Quantity every 10th + 4 record
        'Price': round(random.uniform(10, 1000), 2) if index % 10 != 5 else 'InvalidPrice',  # Invalid Price every 10th + 5 record
        'Date_and_Time_When_Order_Was_Placed': datetime.now() - timedelta(days=random.randint(1, 365)),
        'Customer_Country': random.choice(COUNTRIES),
        'Customer_City': f'City_{index}' if index % 10 != 6 else 'InvalidCity',  # Invalid City every 10th + 6 record
        'Site_From_Where_Order_Was_Placed': random.choice(SITES),
        'Payment_Transaction_Confirmation_Id': UUID_LIST[index] if index % 10 != 7 else 'InvalidUUID',  # Invalid Transaction ID every 10th + 7 record
        'Payment_Success_or_Failure': random.choice(PAYMENT_STATUS),
        'Payment_Failure_Reason': random.choice(FAILURE_REASONS) if random.choice(PAYMENT_STATUS) == 'N' else None
    }
    
    return record

def generate_records(num_records: int) -> pd.DataFrame:
    """Generate a DataFrame containing a specified number of order records."""
    records = [generate_record(i) for i in range(num_records)]
    return pd.DataFrame(records, columns=COLUMNS)

def save_to_csv(dataframe: pd.DataFrame, file_path: str):
    """Save the DataFrame to a CSV file."""
    dataframe.to_csv(file_path, mode='w', header=True, index=False)
    print(f"Data saved to {file_path}")

def display_dataframe_info(dataframe: pd.DataFrame):
    """Display the column names and the first few rows of the DataFrame."""
    print("Column Names:")
    print(dataframe.columns.tolist())
    print("DataFrame Head:")
    print(dataframe.head())


