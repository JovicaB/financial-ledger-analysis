from typing import Optional, Any, Literal, List

import pandas as pd


class ComponentsFR:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
    
    def _get_aop_value(self, AOP: str, year_index: int) -> str:
        df = self.data.iloc[:, 1:]
        value = df.loc[self.data['AOP'] == AOP, df.columns[year_index]].values[0]
        return value
    
    def zalihe(self, year: int) -> int:
        return self._get_aop_value('0031', year)
    
    def obrtna_imovina(self, year: int) -> int:
        return self._get_aop_value('0030', year)
    
    def kupci(self, year: int) -> int:
        return self._get_aop_value('0038', year) 
       
    def kapital(self, year: int) -> int:
        return self._get_aop_value('0401', year) - self._get_aop_value('0403', year) - self._get_aop_value('0455', year) 

    def kratkorocne_obaveze(self, year: int) -> int:
        return self._get_aop_value('0431', year)
    
    def ukupne_obaveze(self, year: int) -> int:
        return self._get_aop_value('0420', year) + self._get_aop_value('0431', year) + self._get_aop_value('0432', year)
    
    def ukupna_imovina(self, year: int) -> int:
        return self._get_aop_value('0002', year) + self._get_aop_value('0030', year)
    
    def poslovna_imovina(self, year: int) -> int:
        return self._get_aop_value('0002', year) - self._get_aop_value('0018', year) + self._get_aop_value('0030', year) - self._get_aop_value('0048', year)
    
    def dugorocne_obaveze(self, year: int) -> int:
        return self._get_aop_value('0420', year)

    def poslovni_dobitak(self, year: int) -> int:
        return self._get_aop_value('1025', year)
    
    def neto_dobit(self, year: int) -> int:
        return self._get_aop_value('1055', year) - self._get_aop_value('1056', year) + self._get_aop_value('1052', year) - self._get_aop_value('1053', year)

    def poslovni_dobitak(self, year: int) -> int:
        return self._get_aop_value('1025', year)

    def prihod_od_prodaje(self, year: int) -> int:
        return self._get_aop_value('1001', year)
    
    def prodaja(self, year: int) -> int:
        return self._get_aop_value('1002', year) + self._get_aop_value('1005', year)
    
    def nabavna_vrednost_prodate_robe(self, year: int) -> int:
        return self._get_aop_value('1014', year)
    
    def obaveze_bez_rezervisanja(self, year: int) -> int:
        return self._get_aop_value('0415', year) - self._get_aop_value('0416', year)

    def ebitda(self, year: int) -> int:
        return self._get_aop_value('1025', year) - self._get_aop_value('1026', year) + self._get_aop_value('1020', year)
    
    def prosecne_zalihe(self, year: int) -> int:
        return (self._get_aop_value('0031', year) + self._get_aop_value('0031', year + 1)) / 2

    def prosecne_zalihe_robe(self, year: int) -> int:
        return (self._get_aop_value('0034', year) + self._get_aop_value('0034', year + 1)) / 2
    
    def prosecni_kupci(self, year: int) -> int:
        return (self._get_aop_value('0038', year) + self._get_aop_value('0038', year + 1)) / 2
    
    def broj_zaposlenih(self, year: int) -> int:
        return self._get_aop_value('9005', year)


class ComponentsLedger:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def filter_data(self, accounts: List[str], month: int, transaction_type: Literal['C', 'D'], 
                    operation: Optional[Literal['sum', 'count']] = None) -> pd.DataFrame:
        """
        Filters the ledger data based on accounts, date, and transaction type, and optionally performs an aggregation.
        """
        df = self.data.copy()

        # Validate accounts
        if not any(df['account'].str.startswith(tuple(accounts))):
            raise ValueError(f"None of the accounts in {accounts} match any account in the dataframe.")

        # Validate month
        if month is not None and not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12.")

        # Ensure 'date' is in datetime format if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Filter by month if specified
        if month is not None:
            df = df[df['date'].dt.month == month]

        # Validate transaction type
        if transaction_type not in {'C', 'D'}:
            raise ValueError("transaction_type must be 'C' (Credit) or 'D' (Debit).")

        # Filter based on transaction type
        column_to_keep = 'credit' if transaction_type == 'C' else 'debit'
        
        if transaction_type == 'C':
            df = df[df['credit'] != 0]
        elif transaction_type == 'D':
            df = df[df['debit'] != 0]
            
        df.drop(columns=[col for col in ['debit', 'credit'] if col != column_to_keep], inplace=True)

        # Filter by accounts
        df_filtered_account = df[df['account'].str.startswith(tuple(accounts))]

        # Apply aggregation if specified
        if operation == 'sum':
            return round(df_filtered_account[column_to_keep].sum(), 2)
        elif operation == 'count':
            return df_filtered_account[column_to_keep].count()

        return df_filtered_account
    

# from utils import DynamicArgsUtils

# df_y_2022 = DynamicArgsUtils.load_clean_ledger('2022')
# print(df_y_2022)