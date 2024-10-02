import pandas as pd
import random
from faker import Faker

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
        'Payment_Type',  # Include Payment_Type here
        'Payment_Transaction_Confirmation_Id',
        'Payment_Success_or_Failure',
        'Payment_Failure_Reason'
    ]
    
    df = df[column_order]  # Reorder DataFrame columns
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
        df[column] = df[column].replace('InvalidUUID', fake.uuid4()).replace('InvalidProductId', fake.uuid4()).replace('InvalidCustomerId', fake.uuid4())

def generate_fake_customer_data(df):
    """Generate fake customer data with a consistent relationship between country and city."""
    df['Customer_Country'] = [random.choice(list(countries_cities.keys())) for _ in range(len(df))]
    df['Customer_City'] = df['Customer_Country'].apply(lambda country: random.choice(countries_cities[country]))
    df['Customer_Name'] = [fake.name() for _ in range(len(df))]

def handle_numeric_data(df):
    """Handle numeric fields by replacing invalid values."""
    # Normalize column names
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    # Check if 'Quantity_Ordered' exists
    if 'Quantity_ordered' in df.columns:
        df['Quantity_ordered'] = pd.to_numeric(df['Quantity_ordered'], errors='coerce').fillna(random.randint(1, 5))
        df['Quantity_ordered'] = df['Quantity_ordered'].replace(-1, 1)
    else:
        print("Column 'Quantity_Ordered' not found. Skipping...")

    # Check if 'Price' exists
    if 'Price' in df.columns:
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(round(random.uniform(10, 1000), 2))
    else:
        print("Column 'Price' not found. Skipping...")

def fill_payment_failure_reason(df):
    """Fill in reasons for payment failures."""
    df['Payment_Failure_Reason'] = df['Payment_Failure_Reason'].fillna("No Reason Provided")

def generate_fake_data(df):
    """Generate fake data and handle corrections."""
    df['Product_Category'] = df['Product_Name'].apply(map_product_to_category)
    df.drop(columns=['Product_Name'], inplace=True)
    df['Product_Name'] = df['Product_Category'].apply(lambda category: random.choice(product_data[category]))

    # Handle invalid IDs
    handle_invalid_ids(df)

    # Generate fake customer data (including country-city consistency)
    generate_fake_customer_data(df)

    # Generate payment types
    df['Payment_Type'] = [random.choice(payment_types) for _ in range(len(df))]

    # Handle numeric data
    handle_numeric_data(df)

    # Fill in payment failure reasons
    fill_payment_failure_reason(df)

    return df

def change_column_order(input_file, output_file):
    """Change the order of columns in a CSV file."""
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)
    
    # Specify the desired column order
    column_order = [
        'Order_Id',
        'Customer_Id',
        'Customer_Name',
        'Product_Id',
        'Product_Category',
        'Product_Name',
        'Quantity_Ordered',
        'Price',
        'Date_and_Time_When_Order_Was_Placed',
        'Customer_Country',
        'Customer_City',
        'Site_From_Where_Order_Was_Placed',
        'Payment_Type',  # Include Payment_Type here
        'Payment_Transaction_Confirmation_Id',
        'Payment_Success_or_Failure',
        'Payment_Failure_Reason'
    ]
    
    # Reorder the DataFrame columns
    df = df[column_order]
    
    # Save the reordered DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
