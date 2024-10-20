import pandas as pd
import json
import requests
import sqlite3


class ETLProcessor:
    def __init__(self, url=None, file_path=None, file_type='json'):
        self.url = url
        self.file_path = file_path
        self.file_type = file_type
        self.data = None

    def fetch_data(self):
        """
        Fetches JSON self from a URL or local file and stores it in its raw form.
        """
        if self.url and self.file_type == 'json':
            response = requests.get(self.url)
            if response.status_code == 200:
                raw_data = response.json()
                self.data = raw_data
            else:
                raise ValueError(f"Error fetching self from {self.url}")
        elif self.file_path:
            if self.file_type == 'csv':
                self.data = pd.read_csv(self.file_path)
            elif self.file_type == 'json':
                with open(self.file_path, 'r') as f:
                    self.data = json.load(f)
        else:
            raise ValueError("No valid URL or file path provided.")

        # Summary of the self
        if isinstance(self.data, list):
            num_records = len(self.data)
            num_columns = len(self.data[0].keys()) if len(self.data) > 0 else 0
        elif isinstance(self.data, dict):
            num_records = 1
            num_columns = len(self.data.keys())
        else:
            num_records, num_columns = 0, 0

        raw_summary = {
            'Number of Records': num_records,
            'Number of Columns': num_columns
        }

        return self.data, raw_summary

    def convert_format(self, output_format='csv', output_path=None, db_file=None, table_name=None):
        """
        Converts the JSON self to a CSV file, JSON file, or SQL database.
        """
        if output_format == 'csv':
            self.save_json_as_csv(output_path)
        elif output_format == 'json':
            with open(output_path, 'w') as file:
                json.dump(self.data, file, indent=4)
        elif output_format == 'sql':
            self.store_data(db_file=db_file, table_name=table_name)
        else:
            raise ValueError("Unsupported output format. Please choose 'csv', 'json', or 'sql'.")

        print(f"Data converted and saved as {output_format}.")

    def save_json_as_csv(self, output_path):
        """
        Saves the JSON self as a CSV file.
        """
        if isinstance(self.data, dict):
            df = pd.DataFrame([self.data])
        elif isinstance(self.data, list):
            df = pd.DataFrame(self.data)
        else:
            raise ValueError("The self structure is not suitable for direct CSV conversion.")

        df.to_csv(output_path, index=False)
        print(f"Data successfully saved as CSV at {output_path}.")

    def modify_columns(self, remove_null_threshold=0.5, check_id_column=True):
        """
        this function removes columns with more than 50% null values,
        and optionally adds new columns.
        """
        # remove columns with more than 50% (default) null values
        null_percentage = self.data.isna().mean()
        columns_to_drop = null_percentage[null_percentage > remove_null_threshold].index
        self = self.data.drop(columns=columns_to_drop)

        # add ID column if there is none already and the user says yes
        if check_id_column:
            if 'ID' or 'Rk' not in self.columns:
                # Ask the user if they want to add an ID column
                add_id = input("No 'ID' column found. Would you like to add an ID column? (yes/no): ").strip().lower()
                if add_id == 'yes':
                    self['ID'] = range(1, len(self) + 1)
                    print("ID column added.")
                else:
                    print("ID column not added.")

        return self

    def store_data(self, db_file=None, table_name=None):
        """
        Stores the data in a SQL database after converting unsupported types.
        """
        if db_file is None or table_name is None:
            raise ValueError("SQLite storage requires a database file path and a table name.")

        # ensure self.data is a dataframe
        if isinstance(self.data, pd.DataFrame):
            df = self.data
        elif isinstance(self.data, dict):
            df = pd.DataFrame([self.data])  # Convert dict to DataFrame
        elif isinstance(self.data, list):
            df = pd.DataFrame(self.data)  # Convert list to DataFrame
        else:
            raise ValueError("The data structure is not suitable for SQL storage.")

        # convert columns with unsupported types to strings
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
                df[col] = df[col].apply(lambda x: json.dumps(x))  # Convert to JSON string

        # Connect to the SQLite database and store the DataFrame
        conn = sqlite3.connect(db_file)
        df.to_sql(table_name, conn, if_exists='replace', index=False)  # Write DataFrame to SQL table
        conn.commit()
        conn.close()

        print(f"Data successfully written to the '{table_name}' table in the database '{db_file}'.")

    def generate_summary(self):
        """
        Prints a summary of the self.
        """
        if self.data is not None:
            if isinstance(self.data, list):
                num_records = len(self.data)
                num_columns = len(self.data[0].keys()) if len(self.data) > 0 else 0
            elif isinstance(self.data, dict):
                num_records = 1
                num_columns = len(self.data.keys())
            else:
                num_records, num_columns = 0, 0
            print(f"Post-processing summary: {num_records} records and {num_columns} columns.")
        else:
            print("No self available to summarize.")


# json example
# nutrition fact data taken from the GitHub link in the project instructions
url = 'https://world.openfoodfacts.org/api/v0/product/5060292302201.json'
processor = ETLProcessor(url=url, file_type='json')
data, summary = processor.fetch_data()
print("Data Summary:", summary)
processor.convert_format(output_format='csv', output_path='nutrition_facts.csv')
processor.convert_format(output_format='sql', db_file='nutrition_facts.db', table_name='json_data')
processor.generate_summary()

# 2022 world series self csv
processor = ETLProcessor(file_path='/Users/alicevadney/Downloads/archive/world-series-batting-2022.csv', file_type='csv')
data, summary = processor.fetch_data()
print("Data Summary:", summary)
processor.modify_columns()
processor.convert_format(output_format='sql', db_file='output.db', table_name='batting_stats')
processor.generate_summary()

