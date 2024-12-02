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

    @staticmethod
    def get_account_data(df: pd.DataFrame, account: str | list, debit_or_credit: str = 'all') -> pd.DataFrame:
        """
        Filter data based on the account(s) and optionally the debit or credit column.
        
        Parameters:
        - account: A string or list of account prefixes to filter by.
        - debit_or_credit: The column to filter by ('debit', 'credit', or 'all' for no filter). Default is 'all'.
        
        Returns:
        - Filtered DataFrame with only the relevant columns.
        """
        if debit_or_credit not in ['debit', 'credit', 'all']:
            raise ValueError("The argument 'debit_or_credit' must be 'debit', 'credit', or 'all'.")

        df['account'] = df['account'].astype(str)

        if isinstance(account, str):
            filtered_data = df[df['account'].str.startswith(account)]
        elif isinstance(account, list):
            filtered_data = df[df['account'].str.startswith(tuple(account))]
        else:
            raise ValueError("The 'account' parameter must be a string or a list of strings.")

        if debit_or_credit == 'debit':
            filtered_data = filtered_data[['date', 'account', 'debit']]
        elif debit_or_credit == 'credit':
            filtered_data = filtered_data[['date', 'account', 'credit']]
        else:
            filtered_data = filtered_data[['date', 'account', 'debit', 'credit']]

        return filtered_data

    @staticmethod
    def get_annual_data(df: pd.DataFrame, year: int):
        return df[df['date'].dt.year == year]



# df = pd.read_csv(r"data\csv\financial_journal_2019.csv")
# df = ComponentsLedger.get_account_data(df, '6')
# print(df)