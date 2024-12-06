from typing import Optional, Any, Literal, List

import pandas as pd


class ComponentsFR:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.cache = {}

    def _get_aop_value(self, AOP: str, year_index: int) -> int:
        key = (AOP, year_index)
        if key in self.cache:
            return self.cache[key]
        
        year_column = f"year_{year_index}"
        value = self.data.loc[self.data['AOP'] == AOP, year_column].values[0]
        self.cache[key] = value
        return value
    
    def zalihe(self, year_index: int) -> int:
        return self._get_aop_value('0031', year_index)
    
    def obrtna_imovina(self, year_index: int) -> int:
        return self._get_aop_value('0030', year_index)
    
    def kupci(self, year_index: int) -> int:
        return self._get_aop_value('0038', year_index) 
       
    def kapital(self, year_index: int) -> int:
        return self._get_aop_value('0401', year_index) - self._get_aop_value('0403', year_index) - self._get_aop_value('0455', year_index) 

    def kratkorocne_obaveze(self, year_index: int) -> int:
        return self._get_aop_value('0431', year_index)
    
    def ukupne_obaveze(self, year_index: int) -> int:
        return self._get_aop_value('0420', year_index) + self._get_aop_value('0431', year_index) + self._get_aop_value('0432', year_index)
    
    def ukupna_imovina(self, year_index: int) -> int:
        return self._get_aop_value('0002', year_index) + self._get_aop_value('0030', year_index)
    
    def poslovna_imovina(self, year_index: int) -> int:
        return self._get_aop_value('0002', year_index) - self._get_aop_value('0018', year_index) + self._get_aop_value('0030', year_index) - self._get_aop_value('0048', year_index)
    
    def dugorocne_obaveze(self, year_index: int) -> int:
        return self._get_aop_value('0420', year_index)

    def poslovni_dobitak(self, year_index: int) -> int:
        return self._get_aop_value('1025', year_index)
    
    def neto_dobit(self, year_index: int) -> int:
        return self._get_aop_value('1055', year_index) - self._get_aop_value('1056', year_index) + self._get_aop_value('1052', year_index) - self._get_aop_value('1053', year_index)

    def poslovni_dobitak(self, year_index: int) -> int:
        return self._get_aop_value('1025', year_index)

    def prihod_od_prodaje(self, year_index: int) -> int:
        return self._get_aop_value('1001', year_index)
    
    def prodaja(self, year_index: int) -> int:
        return self._get_aop_value('1002', year_index) + self._get_aop_value('1005', year_index)
    
    def nabavna_vrednost_prodate_robe(self, year_index: int) -> int:
        return self._get_aop_value('1014', year_index)
    
    def obaveze_bez_rezervisanja(self, year_index: int) -> int:
        return self._get_aop_value('0415', year_index) - self._get_aop_value('0416', year_index)

    def ebitda(self, year_index: int) -> int:
        return self._get_aop_value('1025', year_index) - self._get_aop_value('1026', year_index) + self._get_aop_value('1020', year_index)
    
    def prosecne_zalihe(self, year_index: int) -> int:
        zalihe_curr = self._get_aop_value('0031', year_index)
        zalihe_next = self._get_aop_value('0031', year_index + 1)
        return (zalihe_curr + zalihe_next) // 2

    def prosecne_zalihe_robe(self, year_index: int) -> int:
        zalihe_curr = self._get_aop_value('0034', year_index)
        zalihe_next = self._get_aop_value('0034', year_index + 1)
        return (zalihe_curr + zalihe_next) // 2
    
    def prosecni_kupci(self, year_index: int) -> int:
        kupci_curr = self._get_aop_value('0034', year_index)
        kupci_next = self._get_aop_value('0034', year_index + 1)
        return (kupci_curr + kupci_next) // 2
    
    def broj_zaposlenih(self, year_index: int) -> int:
        return self._get_aop_value('9005', year_index)


## USAGE ##
# df = pd.read_parquet(r"data\parquet\financial_reports.parquet")
# # ComponentsFR(df)._get_aop_value('0002', 1)
# print(ComponentsFR(df).prihod_od_prodaje(1))

class ComponentsLedger:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def get_account_data(self, account: str | list, debit_or_credit: str = 'all') -> pd.DataFrame:
        """
        Filter data based on the account(s) and optionally the debit or credit column.
        
        Parameters:
        - account: A string or list of account prefixes to filter by.
        - debit_or_credit: The column to filter by ('debit', 'credit', or 'all' for no filter). Default is 'all'.
        
        Returns:
        - Filtered DataFrame with only the relevant columns.
        """
        df = self.data

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

    def sum_account_data_by_month(self, account: str | list, debit_or_credit: str = 'all') -> dict:
        """
        Summarize data by month and year, optionally filtering by account(s) and debit or credit.

        Parameters:
        - account: A string or list of account prefixes to filter by.
        - debit_or_credit: The column to filter by ('debit', 'credit', or 'all' for no filter). Default is 'all'.

        Returns:
        - Dictionary with 'month-year' as keys and sums as values.
        """
        df = self.data.copy()

        if debit_or_credit not in ['debit', 'credit', 'all']:
            raise ValueError("The argument 'debit_or_credit' must be 'debit', 'credit', or 'all'.")

        df['account'] = df['account'].astype(str)

        if isinstance(account, str):
            filtered_data = df[df['account'].str.startswith(account)]
        elif isinstance(account, list):
            filtered_data = df[df['account'].str.startswith(tuple(account))]
        else:
            raise ValueError("The 'account' parameter must be a string or a list of strings.")

        filtered_data['year'] = filtered_data['date'].dt.year
        filtered_data['month'] = filtered_data['date'].dt.month

        if debit_or_credit == 'debit':
            filtered_data = filtered_data[['year', 'month', 'debit']]
        elif debit_or_credit == 'credit':
            filtered_data = filtered_data[['year', 'month', 'credit']]
        else:
            filtered_data = filtered_data[['year', 'month', 'debit', 'credit']]

        cols_to_sum = ['debit', 'credit']
        cols_in_data = [col for col in cols_to_sum if col in filtered_data.columns]
        grouped_data = (
            filtered_data.groupby(['year', 'month'], as_index=False)[cols_in_data]
            .sum()
        )

        grouped_data['month_year'] = grouped_data['year'].astype(str) + '-' + grouped_data['month'].astype(str).str.zfill(2)

        result = round(grouped_data.set_index('month_year')[cols_in_data].sum(axis=1)).to_dict()

        return result

    @staticmethod
    def get_annual_data(df: pd.DataFrame, year: int):
        return df[df['date'].dt.year == year]

    @staticmethod
    def calculate_percentage_changes_from_100(df, column):
        percentage_changes = [100.0]
        
        for i in range(1, len(df)):
            change = ((df[column].iloc[i] - df[column].iloc[i - 1]) / df[column].iloc[i - 1]) * 100
            percentage_changes.append(round(change, 2))
        
        df[f'{column}_pct_change'] = percentage_changes
        return df






# data = {
#     'year': [2019, 2020, 2021, 2022, 2023],
#     'debit': [383534.00, 178067.35, 1210649.00, 14722612.50, 1619559.50]
# }
# df = pd.DataFrame(data)

# # Apply the function
# df = ComponentsLedger.calculate_percentage_changes_from_100(df, 'debit')
# print(df)

# USAGE
# years = [2019, 2020, 2021, 2022, 2023]
# df_list = []

# for year in years:
#     df_list.append(pd.read_parquet(f"data/parquet/financial_journal_{year}.parquet"))

# df = pd.concat(df_list, ignore_index=True)

# df['date'] = pd.to_datetime(df['date'])
# df['date'] = pd.to_datetime(df['date'])

# df = df[~((df['date'].dt.month == 1) & (df['date'].dt.day == 1))]
# df = df[~(df['account'].str.startswith(('599', '699', '7')))]

# df = df.reset_index(drop=True)
# # ----------------------------------------------------------------------- #
# class_inst = ComponentsLedger(df)
# print(class_inst.sum_account_data_by_month('02', 'credit'))