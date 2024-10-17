import pandas as pd
import random
from faker import Faker
import streamlit as st

# Initialize the Faker generator
fake = Faker()

# Define the structured product data with relationships
product_data = {
    "Electronics": [
        "Smartphones", "Laptops", "Headphones", "Chargers", "Batteries"
    ],
    "Clothing": [
        "T-Shirts", "Jeans", "Jackets", "Socks", "Sweaters"
    ],
    "Home & Kitchen": [
        "Toothpaste", "Shampoo", "Soap", "Lotion", "Detergent"
    ],
    "Books": [
        "Fiction", "Non-Fiction", "Comics", "Textbooks", "Magazines"
    ],
    "Sports": [
        "Football", "Tennis Racket", "Cricket Bat", "Basketball", "Gym Gloves"
    ]
}

# List of possible payment types
payment_types = ['Card', 'Internet Banking', 'UPI', 'Wallet']

# Define country-city relationship
countries_cities = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'UK': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow'],
    'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg', 'Cologne'],
    'India': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa']
}

def load_data(input_csv_file):
    """Load data from a CSV file into a DataFrame."""
    return pd.read_csv(input_csv_file)

def save_data(df, output_csv_file):
    """Save processed DataFrame to a CSV file with specific column order."""
    column_order = [
        'Order_Id',
        'Customer_Id',
        'Customer_Name',
        'Product_Id',
        'Product_Category',
        'Product_Name',
        'Quantity_ordered',
        'Price',
        'Date_and_Time_When_Order_Was_Placed',
        'Customer_Country',
        'Customer_City',
        'Site_From_Where_Order_Was_Placed',
        'Payment_Type',
        'Payment_Transaction_Confirmation_Id',
        'Payment_Success_or_Failure',
        'Payment_Failure_Reason'
    ]
    
    # Filter the DataFrame to include only the specified columns that exist
    df = df[column_order] if set(column_order).issubset(df.columns) else df
    df.to_csv(output_csv_file, mode='w', header=True, index=False)

def map_product_to_category(product_name):
    """Map product names to categories based on structured product_data."""
    for category, products in product_data.items():
        if product_name in products:
            return category
    return random.choice(list(product_data.keys()))  # Fallback to a random category if not found

def handle_invalid_ids(df):
    """Replace invalid IDs with newly generated UUIDs."""
    invalid_id_columns = ['Product_Id', 'Order_Id', 'Customer_Id', 'Payment_Transaction_Confirmation_Id']
    for column in invalid_id_columns:
        if column in df.columns:
            df[column] = df[column].replace('InvalidUUID', fake.uuid4()).replace('InvalidProductId', fake.uuid4()).replace('InvalidCustomerId', fake.uuid4())

def generate_fake_customer_data(df):
    """Generate fake customer data with a consistent relationship between country and city."""
    if any(col in df.columns for col in ['Customer_Country', 'Customer_City', 'Customer_Name']):
        df['Customer_Country'] = [random.choice(list(countries_cities.keys())) for _ in range(len(df))]
        df['Customer_City'] = df['Customer_Country'].apply(lambda country: random.choice(countries_cities[country]))
        df['Customer_Name'] = [fake.name() for _ in range(len(df))]

def handle_numeric_data(df):
    """Handle numeric fields by replacing invalid values."""
    # Normalize column names
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    # Check if 'Quantity_ordered' exists
    if 'Quantity_ordered' in df.columns:
        df['Quantity_ordered'] = pd.to_numeric(df['Quantity_ordered'], errors='coerce').fillna(random.randint(1, 5))
        df['Quantity_ordered'] = df['Quantity_ordered'].replace(-1, 1)

    # Check if 'Price' exists
    if 'Price' in df.columns:
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(round(random.uniform(10, 1000), 2))

def fill_payment_failure_reason(df):
    """Fill in reasons for payment failures if the column exists."""
    if 'Payment_Failure_Reason' in df.columns:
        df['Payment_Failure_Reason'] = df['Payment_Failure_Reason'].fillna("No Reason Provided")

def generate_fake_data(df, selected_columns):
    """Generate fake data and handle corrections for selected columns."""
    # Handle invalid IDs for selected columns
    handle_invalid_ids(df)

    # Generate fake customer data if related columns are selected
    if any(col in selected_columns for col in ['Customer_Country', 'Customer_City', 'Customer_Name']):
        generate_fake_customer_data(df)

    # Generate product category and product name
    if 'Product_Name' in selected_columns:
        df['Product_Category'] = df['Product_Name'].apply(map_product_to_category)
        df['Product_Name'] = df['Product_Category'].apply(lambda category: random.choice(product_data[category]))

    # Generate payment types if column is selected
    if 'Payment_Type' in selected_columns:
        df['Payment_Type'] = [random.choice(payment_types) for _ in range(len(df))]

    # Handle numeric data if related columns are selected
    if any(col in selected_columns for col in ['Quantity_ordered', 'Price']):
        handle_numeric_data(df)

    # Fill in payment failure reasons if the column is selected
    fill_payment_failure_reason(df)

    # Keep only selected columns that are present in the DataFrame
    return df[selected_columns] if selected_columns else df  # Return original DataFrame if no columns selected
