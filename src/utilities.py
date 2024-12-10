import json
import os
import numpy as np
import pandas as pd
import duckdb
import sqlite3
from typing import Any


class Utilities:

    @staticmethod
    def get_account_description(account: str) -> str:
        account_map_path = os.path.join(os.path.dirname(__file__), "../data/accounts_map.json")
        account = account[:3]

        with open(account_map_path, "r", encoding="utf-8") as file:
            account_map = json.load(file)

        return account_map.get(account[:3], "Konto nije pronađen")
    
    @staticmethod
    def convert_csv_to_parquet(csv_file_path):
        directory_path = os.path.dirname(csv_file_path)
        filename_without_ext = os.path.splitext(os.path.basename(csv_file_path))[0]
        parquet_filename = filename_without_ext + ".parquet"
        parquet_file_path = os.path.join(directory_path, parquet_filename)
        parquet_file_path = parquet_file_path.replace("\\", "/")

        duckdb.sql(f"""
            COPY (SELECT * FROM read_csv_auto('{csv_file_path}'))
            TO '{parquet_file_path}'
            (FORMAT PARQUET)
        """)

        return f"File {filename_without_ext} successfully converted to parquet format"

    @staticmethod
    def save_results(database_fullname: str, description: str, result: dict):
        result_converted = Utilities._convert_to_native_types(result)

        conn = sqlite3.connect(database_fullname)
        # Use INSERT OR REPLACE to update if description exists
        conn.execute("""
            INSERT OR REPLACE INTO results (description, result) 
            VALUES (?, ?)
        """, (description, str(result_converted)))
        conn.commit()
        conn.close()
    # def save_results(database_fullname: str, description: str, result: dict):
    #     result_converted = Utilities._convert_to_native_types(result)

    #     conn = sqlite3.connect(database_fullname)
    #     conn.execute("INSERT INTO results (description, result) VALUES (?, ?)", 
    #                  (description, str(result_converted))) 
    #     conn.commit()
    #     conn.close()

    @staticmethod
    def _convert_to_native_types(obj):
        """
        Convert numpy types, pandas types, and other non-native Python types to native Python types.
        This avoids issues with JSON serialization.
        """
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat() 
        elif isinstance(obj, (np.int64, np.int32)):  
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)): 
            return float(obj)
        elif isinstance(obj, pd.Series):  
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame): 
            return obj.to_dict(orient='records')
        elif isinstance(obj, dict): 
            return {k: Utilities._convert_to_native_types(v) for k, v in obj.items()}
        return obj 



        conn.close()

# database_name = "C:\\xxx.db"
# description = "Sample description"
# data = {"key1": "value1", "key2": [1, 2, 3]}
# Utilities.save_results(database_name, description, data)
# print(Utilities.get_account_description("02255"))
# Utilities.convert_csv_to_parquet(r'data\csv\financial_journal_2019.csv')