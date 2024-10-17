import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
import seaborn as sns
from gcs import GCSHandler 
from data_generator import write_to_csv
from rough_data_generation import generate_records as generate_rough_data
from rough_data_generation import save_to_csv
from data_handling import load_data, save_data, generate_fake_data
from merge import merge_csv_files, check_duplicates, parse_dates, show_info

# Initialize the GCSHandler
gc = GCSHandler()

# App Layout and Color Palette Setup
st.set_page_config(layout="wide")  # Set wide layout for the app

# Custom Styling for Headers and Buttons
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
        color: #34495E;
    }
    .header {
        font-size: 36px;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
    }
    .section-title {
        font-size: 28px;
        color: #2980B9;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .subsection-title {
        font-size: 20px;
        color: #34495E;
        font-weight: bold;
    }
    .success-text {
        color: #27AE60;
        font-size: 18px;
    }
    .error-text {
        color: #E74C3C;
        font-size: 18px;
    }
    .button-style {
        background-color: #3498DB;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .button-style:hover {
        background-color: #2980B9;
    }
    .deleted-label {
        position: absolute;
        top: 10px;
        left: 10px;
        color: #E74C3C;
        font-size: 24px;
        font-weight: bold;
    }
    .file-upload {
        margin-bottom: 20px;
    }
    .gcs-section {
        margin-top: 40px;
        border: 1px solid #2980B9;
        border-radius: 10px;
        padding: 20px;
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("E-Commerce Analytical HUB")


# Display "Deleted" label at the top left
st.markdown("<div class='deleted-label'>Deleted</div>", unsafe_allow_html=True)

# Button to show project details
if st.button("About Project", key='about_project_button'):
    st.markdown("""
    ### Project Overview: E-Com Insight Pipeline
    The **E-Com Insight Pipeline** is a comprehensive data engineering initiative aimed at optimizing the generation, cleansing, analysis, and visualization of E-Commerce data. This project is designed to provide the Analytics team with actionable insights derived from large-scale data, facilitating well-informed business decisions for stakeholders.
    
    #### Key Components:
    1. Data Generation
    2. Exploratory Data Analysis (EDA) and Data Cleansing
    3. Data Upload
    4. Data Loading
    5. Data Analysis
    6. Data Visualization
    
    ### Objectives:
    - Develop a Python program for generating CSV data.
    - Perform EDA and cleanse data.
    - Upload to Google Cloud Storage and analyze using BigQuery.
    - Create visualizations for decision-making.
    """)

# Section 1: Data Generation
st.markdown("<div class='section-title'>1. Data Generation</div>", unsafe_allow_html=True)

# Select Columns to Generate
all_columns = ["Order_Id", "Customer_Id", "Customer_Name", "Product_Id", "Product_Category", 
               "Product_Name", "Payment_Type", "Quantity_ordered", "Price", 
               "Date_and_Time_When_Order_Was_Placed", "Customer_Country", 
               "Customer_City", "Site_From_Where_Order_Was_Placed", 
               "Payment_Transaction_Confirmation_Id", "Payment_Success_or_Failure", 
               "Payment_Failure_Reason"]

selected_columns = st.multiselect(
    "Select columns for data generation", all_columns, default=all_columns
)
num_records = st.number_input("Number of records to generate", min_value=1, max_value=100000, value=1000)

if st.button('Generate Data', key='generate_data_button'):
    file_name = 'data_generation.csv'
    write_to_csv(file_name, num_records, selected_columns)
    data = pd.read_csv(file_name)
    rough_file_location = os.path.abspath(file_name)  # Get absolute path for the file

    # Success message with file location
    st.success(f"{num_records} records generated successfully! The file is stored at: {rough_file_location}")
    st.write(data.head())  # Display the first few rows of the generated data

    # Print the file location to the console
    print(f"The file is stored at: {rough_file_location}")

# Section 2: Rough Data Generation
st.markdown("<div class='section-title'>2. Rough Data Generation</div>", unsafe_allow_html=True)

rough_columns = all_columns

# Allow users to select the columns they want to include in the rough data generation
selected_rough_columns = st.multiselect(
    "Select columns for rough data generation", rough_columns, default=rough_columns
)

num_rough_records = st.number_input("How many rough records to generate?", min_value=1, max_value=100000, value=1000)

if st.button('Generate Rough Data', key='generate_rough_data_button'):
    rough_file_name = 'rough_data_generation.csv'
    rough_data = generate_rough_data(num_rough_records, selected_rough_columns)
    save_to_csv(rough_data, rough_file_name)
    rough_file_location = os.path.abspath(rough_file_name)  # Get absolute path for the file

    # Success message with file location
    st.success(f"{num_rough_records} rough records generated successfully! The file is stored at: {rough_file_location}")
    st.write(rough_data.head())  # D
# Section 3: Data Handling & Standardization
st.markdown("<div class='section-title'>3. Data Handling & Standardization</div>", unsafe_allow_html=True)

input_file = st.file_uploader("Upload your rough data CSV file:", type=['csv'], key='file_uploader', label_visibility="collapsed")
output_file = st.text_input("Enter the output filename (with .csv extension):", value='handling_rough_data.csv', key='output_filename')

# Define available columns for selection
available_columns = all_columns

selected_columns = st.multiselect("Select columns to include in the processed data:", available_columns, default=available_columns)

if st.button('Process Data', key='process_data_button'):
    if input_file and output_file:
        try:
            df = load_data(input_file)  # Load DataFrame from CSV
            
            # Keep only the selected columns that are available in the DataFrame
            valid_selected_columns = [col for col in selected_columns if col in df.columns]
            df = df[valid_selected_columns]  # Filter DataFrame to only selected columns
            
            # Generate fake data using the DataFrame
            df = generate_fake_data(df, valid_selected_columns)  # Pass selected columns to the function
            
            # Save the processed DataFrame
            save_data(df, output_file)  
            
            # Get the absolute path of the output file
            output_file_location = os.path.abspath(output_file)
            
            # Success message with file location
            st.success(f"Data processed and saved to '{output_file_location}'")
            st.write(df.head())  # Display the first few rows of the DataFrame
            
            # Print the file location to the console
            print(f"Processed data saved at: {output_file_location}")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please upload a CSV file and provide a valid output filename.")

# Section 4: CSV File Merging
st.markdown("<div class='section-title'>4. CSV File Merging</div>", unsafe_allow_html=True)

file1 = st.text_input("Enter the path of the first CSV file:", key='file1_input')
file2 = st.text_input("Enter the path of the second CSV file:", key='file2_input')

if st.button("Merge CSV Files", key='merge_files_button'):
    if file1 and file2:
        merged_data = merge_csv_files(file1, file2)
        if merged_data is not None:
            st.write("Merged CSV Preview:")
            st.write(merged_data.head())

            # Save the merged DataFrame to a CSV file
            output_file = 'final_data.csv'
            merged_data.to_csv(output_file, index=False)
            
            # Get the absolute path of the output file
            output_file_location = os.path.abspath(output_file)
            
            # Success message with file location
            st.success(f"CSV files merged and saved as '{output_file_location}'")
            
            # Print the file location to the console
            print(f"Merged data saved at: {output_file_location}")
    else:
        st.error("Please provide both file paths.")

if st.button("Check for Duplicates", key='check_duplicates_button'):
    try:
        final_data = pd.read_csv('final_data.csv')
        duplicates = check_duplicates(final_data)
        st.write(f"Number of duplicate rows: {duplicates}")
    except Exception as e:
        st.error(f"Error: {e}")
# Section for Displaying DataFrame Information

if st.button("Show DataFrame Info", key='info_button'):
    try:
        # Load the data
        final_data = pd.read_csv('final_data.csv')
        
        # DataFrame Information
        shape = final_data.shape
        column_names = final_data.columns.tolist()
        data_types = final_data.dtypes.astype(str).tolist()  # Convert data types to strings for display

        # Create columns for the display
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Shape of DataFrame:")
            st.write(f"{shape}")  # Displays (rows, columns)

        with col2:
            st.subheader("Column Names:")
            st.write(column_names)  # Lists all column names

        with col3:
            st.subheader("Data Types:")
            st.write(data_types)  # Displays data types of each column
        
        # Optionally display a preview of the DataFrame
        st.write("Preview of the DataFrame:")
        st.dataframe(final_data.head())  # Displays the first few rows of the DataFrame

    except Exception as e:
        st.error(f"Error: {e}")

        
# Section 5: Uploading to Google Cloud Storage (GCS)
st.markdown("<div class='section-title'>5. Upload to Google Cloud Storage (GCS)</div>", unsafe_allow_html=True)

# Expecting a string input for the GCS bucket name
bucket_name: str = st.text_input("Enter GCS bucket name:", key='bucket_name_input')

# Create GCS Bucket Button
if st.button("Create GCS Bucket", key='create_bucket_button'):
    if bucket_name:
        result = gc.create_bucket(bucket_name)
        # Display success or error message based on the result
        if "successfully" in result:
            st.success(result)
        else:
            st.error(result)
    else:
        st.error("Please enter a bucket name.")
# Delete GCS Bucket Button
if st.button("Delete GCS Bucket", key='delete_bucket_button'):
    if bucket_name:
        result = gc.delete_bucket(bucket_name)
        # Display success or error message based on the result
        if "successfully" in result:
            st.success(result)
        else:
            st.error(result)
    else:
        st.error("Please enter a bucket name to delete.")

if st.button("List GCS Buckets", key='list_buckets_button'):
    result = gc.list_buckets()
    st.write(result)

if st.button("List Files in GCS Bucket", key='list_files_button'):
    if bucket_name:
        result = gc.list_files_in_bucket(bucket_name)
        st.write(result)
    else:
        st.error("Please enter a bucket name.")
        
        
uploaded_file = st.file_uploader("Choose a file to upload", type=['csv', 'txt', 'jpg', 'png'])

# Button to upload the selected file
if st.button("Upload File to GCS", key='upload_file_button'):
    if uploaded_file is not None and bucket_name:
        # Get the destination file name
        destination_file_name = uploaded_file.name
        
        # Use a temporary file to save the uploaded file
        with open(destination_file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Call the upload_blob method and capture the return message
        message = gc.upload_blob(bucket_name, destination_file_name, destination_file_name)
        
        # Optionally delete the temporary file if necessary
       # os.remove(destination_file_name)  # Clean up the temporary file if needed

        st.success(message)  # Display the success message
    elif uploaded_file is None:
        st.error("Please select a file to upload.")
    else:
        st.error("Please enter a bucket name.")
        
# Input for the blob name to delete
blob_name = st.text_input("Enter the name of the file to delete from the GCS bucket:", key='blob_name_input')

if st.button("Delete File from GCS", key='delete_blob_button'):
    if bucket_name and blob_name:
        result = gc.delete_blob(bucket_name, blob_name)  # Call the delete_blob method
        
        # Check if the deletion was successful
        if "deleted" in result:
            st.success(result)
        else:
            st.error(result)
    else:
        st.error("Please enter both a bucket name and a file name to delete.")


# Set seaborn style for better aesthetics
sns.set(style="whitegrid")

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('final_data.csv')

df = load_data()

# Section 6: Queries Section
st.markdown("<div class='section-title'>6. Queries Section</div>", unsafe_allow_html=True)

# Function to plot DataFrame data
def plot_data(df, title, x_label, y_label):
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df, x=x_label, y=y_label)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

# Function to handle each predefined query
def display_query_1():
    top_category_per_country = df.groupby(['Customer_Country', 'Product_Category']).agg({'Quantity_ordered': 'sum'}).reset_index()
    top_category_per_country = top_category_per_country.sort_values(by='Quantity_ordered', ascending=False).groupby('Customer_Country').head(1)

    # Create two columns for output and plot
    col1, col2 = st.columns(2)

    with col1:
        st.write(top_category_per_country)

    with col2:
        plot_data(top_category_per_country, 'Top-Selling Category of Items per Country', 'Customer_Country', 'Quantity_ordered')
        st.pyplot(plt)
        plt.clf()  # Clear the figure after displaying

def display_query_2():
    df['Date_and_Time_When_Order_Was_Placed'] = pd.to_datetime(df['Date_and_Time_When_Order_Was_Placed'], errors='coerce')
    df['Month'] = df['Date_and_Time_When_Order_Was_Placed'].dt.month
    product_popularity = df.groupby(['Customer_Country', 'Month', 'Product_Name']).agg({'Quantity_ordered': 'sum'}).reset_index()

    # Create two columns for output and plot
    col1, col2 = st.columns(2)

    with col1:
        st.write(product_popularity)

    with col2:
        plt.figure(figsize=(6, 6))
        sns.lineplot(data=product_popularity, x='Month', y='Quantity_ordered', hue='Customer_Country', marker='o')
        plt.title('Popularity of Products Throughout the Year per Country')
        plt.xlabel('Month')
        plt.ylabel('Quantity Ordered')
        plt.legend(title='Country')
        st.pyplot(plt)
        plt.clf()

def display_query_3():
    highest_traffic_locations = df.groupby(['Customer_Country', 'Customer_City']).agg({'Order_Id': 'count'}).reset_index()
    highest_traffic_locations = highest_traffic_locations.sort_values(by='Order_Id', ascending=False)

    # Create two columns for output and plot
    col1, col2 = st.columns(2)

    with col1:
        st.write(highest_traffic_locations.head(10))  # Top 10 locations

    with col2:
        plot_data(highest_traffic_locations.head(10), 'Top 10 Locations with Highest Traffic for Sales', 'Customer_City', 'Order_Id')
        st.pyplot(plt)
        plt.clf()

def display_query_4():
    df['Date_and_Time_When_Order_Was_Placed'] = pd.to_datetime(df['Date_and_Time_When_Order_Was_Placed'], errors='coerce')
    df['Hour'] = df['Date_and_Time_When_Order_Was_Placed'].dt.hour
    sales_traffic_per_time = df.groupby(['Customer_Country', 'Hour']).agg({'Order_Id': 'count'}).reset_index()

    # Create two columns for output and plot
    col1, col2 = st.columns(2)

    with col1:
        st.write(sales_traffic_per_time)

    with col2:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=sales_traffic_per_time, x='Hour', y='Order_Id', hue='Customer_Country', marker='o')
        plt.title('Sales Traffic per Hour per Country')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Sales Count')
        plt.legend(title='Country')
        st.pyplot(plt)
        plt.clf()

def display_query_5():
    df['Total_Order_Value'] = df['Quantity_ordered'] * df['Price']
    avg_order_value_per_category = df.groupby(['Customer_Country', 'Product_Category']).agg({'Total_Order_Value': 'mean'}).reset_index()

    # Create two columns for output and plot
    col1, col2 = st.columns(2)

    with col1:
        st.write(avg_order_value_per_category)

    with col2:
        plot_data(avg_order_value_per_category, 'Average Order Value per Product Category per Country', 'Customer_Country', 'Total_Order_Value')
        st.pyplot(plt)
        plt.clf()

def display_query_6():
    payment_impact = df.groupby(['Customer_Country', 'Payment_Type', 'Payment_Success_or_Failure']).agg({'Order_Id': 'count'}).reset_index()

    # Create two columns for output and plot
    col1, col2 = st.columns(2)

    with col1:
        st.write(payment_impact)

    with col2:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=payment_impact, x='Payment_Type', y='Order_Id', hue='Payment_Success_or_Failure')
        plt.title('Impact of Payment Methods on Sales Volume per Country')
        plt.xlabel('Payment Method')
        plt.ylabel('Sales Count')
        plt.legend(title='Payment Success or Failure')
        st.pyplot(plt)
        plt.clf()

def display_query_7():
    failure_df = df[df['Payment_Success_or_Failure'] == 'N']
    failure_analysis = failure_df.groupby(['Customer_Country', 'Payment_Failure_Reason']).agg(
        failure_count=('Payment_Transaction_Confirmation_Id', 'count')
    ).reset_index()

    failure_analysis_sorted = failure_analysis.sort_values(by=['Customer_Country', 'failure_count'], ascending=[True, False])

    # Create two columns for output and plot
    col1, col2 = st.columns(2)

    with col1:
        st.write(failure_analysis_sorted)

    with col2:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=failure_analysis_sorted, x='Payment_Failure_Reason', y='failure_count', hue='Customer_Country')
        plt.title('Common Reasons for Payment Failures per Country')
        plt.xlabel('Failure Reason')
        plt.ylabel('Failure Count')
        plt.xticks(rotation=45)
        plt.legend(title='Country')
        st.pyplot(plt)
        plt.clf()


# Query Selection
query_options = [
    "Select a Query",
    "Top-Selling Category of Items per Country",
    "Popularity of Products Throughout the Year per Country",
    "Highest Traffic Locations for Sales",
    "Times with Highest Sales Traffic per Country",
    "Average Order Value per Product Category per Country",
    "Impact of Payment Methods on Sales Volume and Success Rates per Country",
    "Common Reasons for Payment Failures per Country"
]

selected_query = st.selectbox("Choose a predefined query to view results:", query_options)

if selected_query == query_options[1]:
    display_query_1()
elif selected_query == query_options[2]:
    display_query_2()
elif selected_query == query_options[3]:
    display_query_3()
elif selected_query == query_options[4]:
    display_query_4()
elif selected_query == query_options[5]:
    display_query_5()
elif selected_query == query_options[6]:
    display_query_6()
elif selected_query == query_options[7]:
    display_query_7()
    
# Ad Hoc Query Section
st.markdown("<div class='section-title'>7 Ad Hoc Query Section</div>", unsafe_allow_html=True)
st.write("""
This section allows you to run your own SQL-like queries on the dataset. 
Please ensure your query is valid for execution.
""")
user_query = st.text_area("Write your query here:")


if st.button("Execute Ad Hoc Query"):
    try:
        # Check for simple queries using the query method
        if any(op in user_query for op in ['==', '!=', '>', '<', '>=', '<=']):
            query_result = df.query(user_query)
        else:
            # For more complex queries like groupby, use eval or standard DataFrame methods
            exec("query_result = " + user_query)  # Use exec for more complex queries

        if not query_result.empty:
            st.write(query_result)
        else:
            st.write("No results found for the given query.")
    except Exception as e:
        st.error(f"Error: {e}")



st.markdown("<div class='footer'>© 2024 E-Com Insight Pipeline. All Rights Reserved-MANOJ R.</div>", unsafe_allow_html=True)


