import pandas as pd
import streamlit as st
import io


def merge_csv_files(file1, file2):
    try:
        # Load CSV files
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        # Append df1 to df2
        appended_df = pd.concat([df2, df1], ignore_index=True)
        return appended_df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to check for duplicate rows
def check_duplicates(df):
    return df.duplicated().sum()

# Function to show concise summary of the DataFrame
def show_info(df):
    buffer = io.StringIO()  # Capture DataFrame info in a StringIO buffer
    df.info(buf=buffer)
    info_str = buffer.getvalue()  # Retrieve the string from the buffer
    return info_str


# Function to parse date column
def parse_dates(df, column_name):
    try:
        # Attempt to parse the date column
        df[column_name] = pd.to_datetime(df[column_name], format='ISO8601')
        return df
    except Exception as e:
        # Display error message if parsing fails
        st.error(f"Error: {e}")
        return None
    
    
    