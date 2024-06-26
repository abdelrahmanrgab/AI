import os
import pandas as pd

def preprocess_csv_files():
    # Directory containing the CSV files
    script_dir = os.path.dirname(__file__)
    directory = os.path.abspath(os.path.join(script_dir, '../raw/historical_Data/'))

    # Get a list of all CSV files in the directory
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

    # Preprocess each CSV file
    for file_name in csv_files:
        # Load the data
        data = pd.read_csv(os.path.join(directory, file_name))

        # Define the list of columns to drop
        columns_to_drop = ['Adj Close', 'Volume', 'Change (%)', 'Change_%']

        # Drop unnecessary columns if they exist (handle variations in column names)
        columns_to_drop_existing = [col for col in columns_to_drop if col in data.columns]
        if columns_to_drop_existing:
            data = data.drop(columns=columns_to_drop_existing, axis=1)

        # Remove all rows with NULL values
        data.dropna(inplace=True)

        # Remove rows with a NULL value in the "Date" column
        data.dropna(subset=['Date'], inplace=True)

        # Remove all duplicates
        data.drop_duplicates(inplace=True)

        # Convert the 'Date' column to the desired format
        data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')

        # Save the preprocessed data to a new CSV file in the same directory as the script file
        output_file_name = file_name.replace('.csv', '_preprocessed.csv')
        output_path = os.path.join(script_dir, output_file_name)
        data.to_csv(output_path, index=False)

# Call the function to preprocess the CSV files
preprocess_csv_files();