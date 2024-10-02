import random
from faker import Faker
import csv

# Initialize Faker instance
fake = Faker()

# Predefined lists
payment_types = ['Card', 'Internet Banking', 'UPI', 'Wallet']
countries_cities = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'UK': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow'],
    'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg', 'Cologne'],
    'India': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa']
}
sites = ['Amazon', 'eBay', 'Flipkart', 'Walmart', 'Shopify']
payment_status = ['Y', 'N']
failure_reasons = ['Insufficient funds', 'Payment gateway error', 'Card expired']

# Mapping of product names to categories
product_data = {
    "Electronics": ["Smartphones", "Laptops", "Headphones", "Chargers", "Batteries"],
    "Clothing": ["T-Shirts", "Jeans", "Jackets", "Socks", "Sweaters"],
    "Home & Kitchen": ["Toothpaste", "Shampoo", "Soap", "Lotion", "Detergent"],
    "Books": ["Fiction", "Non-Fiction", "Comics", "Textbooks", "Magazines"],
    "Sports": ["Football", "Tennis Racket", "Cricket Bat", "Basketball", "Gym Gloves"]
}

# Functions to generate data
class DataGenerator:
    @staticmethod
    def gen_order_id():
        return fake.uuid4()

    @staticmethod
    def gen_customer_id():
        return fake.uuid4()

    @staticmethod
    def gen_customer_name():
        return fake.name()

    @staticmethod
    def gen_product_id():
        return fake.uuid4()

    @staticmethod
    def gen_category_and_product_name():
        category = random.choice(list(product_data.keys()))
        product_name = random.choice(product_data[category])
        return category, product_name

    @staticmethod
    def gen_country_and_city():
        country = random.choice(list(countries_cities.keys()))
        city = random.choice(countries_cities[country])
        return country, city

    @staticmethod
    def gen_payment_type():
        return random.choice(payment_types)

    @staticmethod
    def gen_quantity_ordered():
        return random.randint(1, 5)

    @staticmethod
    def gen_price():
        return round(random.uniform(10, 1000), 2)

    @staticmethod
    def gen_date_and_time_when_order_was_placed():
        return fake.date_time_this_decade()

    @staticmethod
    def gen_site_from_where_order_was_placed():
        return random.choice(sites)

    @staticmethod
    def gen_payment_transaction_confirmation_id():
        return fake.uuid4()

    @staticmethod
    def gen_payment_success_or_failure():
        return random.choice(payment_status)

    @staticmethod
    def gen_payment_failure_reason():
        return random.choice(failure_reasons)

def generate_record():
    country, city = DataGenerator.gen_country_and_city()
    category, product_name = DataGenerator.gen_category_and_product_name()
    payment_success = DataGenerator.gen_payment_success_or_failure()
    return {
        "Order_Id": DataGenerator.gen_order_id(),
        "Customer_Id": DataGenerator.gen_customer_id(),
        "Customer_Name": DataGenerator.gen_customer_name(),
        "Product_Id": DataGenerator.gen_product_id(),
        "Product_Category": category,
        "Product_Name": product_name,
        "Payment_Type":  DataGenerator.gen_payment_type(),
        "Quantity_ordered": DataGenerator.gen_quantity_ordered(),
        "Price": DataGenerator.gen_price(),  
        "Date_and_Time_When_Order_Was_Placed": DataGenerator.gen_date_and_time_when_order_was_placed(),
        "Customer_Country": country,
        "Customer_City": city,
        "Site_From_Where_Order_Was_Placed": DataGenerator.gen_site_from_where_order_was_placed(),
        "Payment_Transaction_Confirmation_Id": DataGenerator.gen_payment_transaction_confirmation_id(),
        "Payment_Success_or_Failure": payment_success,
        "Payment_Failure_Reason": DataGenerator.gen_payment_failure_reason() if payment_success == 'N' else "Payment Successful"
    }

def write_to_csv(file_name, num_records):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=generate_record().keys())
        writer.writeheader()
        for _ in range(num_records):
            writer.writerow(generate_record())

