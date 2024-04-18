import streamlit as st
from pandasai.llm import OpenAI
from pandasai import SmartDataframe, SmartDatalake
import pandas as pd
import os

def create_smart_datalake(folder_path, api_token):
    """
    Creates separate SmartDatalakes for CSV and Excel files in a folder.

    Args:
        folder_path (str): Path to the folder containing data files.
        api_token (str): Your OpenAI API key.

    Returns:
        tuple: A tuple containing two SmartDatalake objects, one for CSV and one for Excel.

    Raises:
        ValueError: If the folder path is invalid.
        IOError: If an error occurs while reading a file.
    """

    csv_dataframes, excel_dataframes = [], []
    llm = OpenAI(api_token=api_token)

    if not os.path.isdir(folder_path):
        raise ValueError(f"Invalid folder path: {folder_path}")

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        try:
            if file_name.endswith('.csv'):
                df = pd.read_csv(file_path)
                smart_df = SmartDataframe(df, config={"llm": llm}, name=file_name)
                csv_dataframes.append(smart_df)
                st.write(f"Successfully read CSV file: {file_name}")
            elif file_name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
                smart_df = SmartDataframe(df, config={"llm": llm}, name=file_name)
                excel_dataframes.append(smart_df)
                st.write(f"Successfully read Excel file: {file_name}")
        except (IOError, pd.errors.ParserError) as e:
            st.write(f"Error reading file: {file_name} - {e}")

    csv_datalake = SmartDatalake(csv_dataframes, config={"llm": llm}) if csv_dataframes else None
    excel_datalake = SmartDatalake(excel_dataframes, config={"llm": llm}) if excel_dataframes else None

    return csv_datalake, excel_datalake

st.title("Smart Data Analysis")

# Get folder path containing CSV or Excel files from user input
folder_path = st.sidebar.text_input("Enter the folder path containing CSV or Excel files:")

# Get OpenAI API token from user input (replace with your actual API token)
api_token = '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'  # Replace with your actual API token

try:
    if folder_path:
        # Create the SmartDatalakes for CSV and Excel files
        csv_datalake, excel_datalake = create_smart_datalake(folder_path, api_token)

        if csv_datalake or excel_datalake:
            # Determine the file type for the query
            file_type = st.sidebar.radio("Select the file type", ('CSV', 'Excel'))
            
            if file_type == 'CSV' and csv_datalake:
                csv_query = st.text_input("Enter your query for CSV files:")
                csv_response = csv_datalake.chat(csv_query)
                st.write(f"Response for CSV files: {csv_response}")
            elif file_type == 'Excel' and excel_datalake:
                excel_query = st.text_input("Enter your query for Excel files:")
                excel_response = excel_datalake.chat(excel_query)
                st.write(f"Response for Excel files: {excel_response}")
            else:
                st.write("Invalid file type or no data available for the specified type.")

except ValueError as e:
    st.error(f"Error: {e}")
