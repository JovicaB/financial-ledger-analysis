import json
import os
import pandas as pd
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

    @staticmethod
    def save_result(output_description: str, output_result: any, output_file="/content/drive/MyDrive/Projects/financial_data_analysis/data/output.csv"):
        """
        Funkcija za snimanje podataka u CSV fajl sa zadatim opisom i rezultatima.
        
        Parameters:
        - output_description: Tekstualni opis koji ide u prvu kolonu.
        - output_result: Rezultat koji može biti bilo koji tip (int, list, dict), koji će biti konvertovan u JSON.
        - output_file: Putanja izlaznog fajla.
        """
        output_result_json = json.dumps(output_result)
        
        df = pd.DataFrame({
            'Opis': [output_description],
            'json_rezultat': [output_result_json]
        })
        
        if os.path.exists(output_file):
            df.to_csv(output_file, index=False, mode='a', header=False)
        else:
            df.to_csv(output_file, index=False)
        
        print(f"Rezultat sačuvan u: {output_file}")

# print(Utilities.get_account_description("02255"))
# Utilities.convert_csv_to_parquet(r'data\csv\financial_journal_2019.csv')