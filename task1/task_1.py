import pandas as pd
import os

FILE_NAME = "data.csv"
file_path = os.path.join(os.getcwd(),FILE_NAME)

def calculate_avg_age(file_path):
    """
    Calculate and print the average age from a CSV file.

    Parameters:
    - file_path (str): Path to the CSV file.

    Raises:
    - FileNotFoundError: If the specified file is not found.
    - pd.errors.EmptyDataError: If the file is empty.
    - pd.errors.ParserError: If there is an issue parsing the CSV file.
    - Exception: For any other unexpected errors.

    Returns:
    - None: Prints the average age if successful.
    """
    try:
        df = pd.read_csv(file_path)
        if 'Name' in df.columns and 'Age' in df.columns:
            # drop individual with missing value in Name or Age
            # task doesnt mention whether missing Name or Value is invalid, so I choose both :D
            df = df.dropna(subset=['Name', 'Age'])
            
            # Check if DataFrame is empty after dropping missing values
            if df.empty:
                print("File is empty or contains all missing values")
            else:
                average_age = df['Age'].mean()
                print(f'The average age is: {average_age}')
        else:
            print('Missing "Age" or "Name" columns')   
    except FileNotFoundError:
        print(f'{file_path} is not found')
    except pd.errors.EmptyDataError:
        print(f'{file_path} is empty')  
    except pd.errors.ParserError:
        print('Unable to parse csv file')
    except Exception as e:
        print(f'Error: {e}')

calculate_avg_age(file_path)