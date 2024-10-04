import json
import os
import duckdb


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


# print(Utilities.get_account_description("02255"))
# Utilities.convert_csv_to_parquet(r'data\csv\financial_journal_2021.csv')
