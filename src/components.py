from typing import Optional, Any, Literal, List, Type

import pandas as pd


class ComponentsFR:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.cache = {}

    def _get_aop_value(self, AOP: str, year: int) -> int:
        key = (AOP, year)
        if key in self.cache:
            return self.cache[key]
        
        # year_column = f"year_{year_index}"
        value = self.data.loc[self.data['AOP'] == AOP, year].values[0]
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

    def prihod_od_prodaje(self, year: int) -> int:
        return self._get_aop_value('1001', year)
    
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

class RatioAnalysis:
    def __init__(self, data: pd.DataFrame, fr_component_obj: Type[object] = None):
        self.df = data
        self.comp_obj = fr_component_obj

   
    def current_ratio(self) -> list[float]:
        """Koeficijent likvidnosti za koga važi generalno pravilo da obrtna imovina 
        treba da bude bar 2 puta veća od kratkoročnih obaveza da bi se smatralo da je 
        likvidnost dobra.
        """
        ratio_results = []

        for year in range(0, 5):
            obrtna_imovina = self.comp_obj.obrtna_imovina(year)
            kratkorocne_obaveze = self.comp_obj.kratkorocne_obaveze(year)
            ratio_results.append(round(float(obrtna_imovina / kratkorocne_obaveze), 2))

        ratio_results.reverse()

        return ratio_results
    
    def quick_ratio(self) -> list[float]:
        """Pokrivenost kratkoročno pozajmljenog kapitala gotovinom, lako unovčivim 
        hartijama od vrednosti i kratkoročnim potraživanjima. Utvrđivanje normale je 
        u korelaciji sa brzinom dospeća kratrkoročnih obaveza. Pokazatelj ne bi trebalo 
        da bude ispod 1.
        """
        ratio_results = []

        for year in range(0, 5):
            obrtna_imovina = self.comp_obj.obrtna_imovina(year)
            zalihe = self.comp_obj.zalihe(year)
            kratkorocne_obaveze = self.comp_obj.kratkorocne_obaveze(year)

            ratio_results.append(round(float((obrtna_imovina - zalihe) / kratkorocne_obaveze), 2))

        ratio_results.reverse()

        return ratio_results
    

    def total_debt_ratio(self) -> list[float]:
        pass
        """Racio pokazuje stepen pokrivenosti obaveza ukupnom 
        imovinom
        """
        ratio_results = []

        for year in range(0, 5):
            ukupne_obaveze = self.components_class_obj.ukupne_obaveze(year)
            ukupna_imovina = self.components_class_obj.ukupna_imovina(year)

            ratio_results.append(round(float(ukupne_obaveze / ukupna_imovina), 2))

        ratio_results.reverse()

        return ratio_results


    def long_term_debt_ratio(self) -> list[float]:
        """Racio pokazuje stepen pokrivenosti dugoročnih 
        obaveza ukupnom imovinom.
        """
        ratio_results = []

        for year in range(0, 5):
            dugorocne_obaveze = self.components_class_obj.dugorocne_obaveze(year)
            ukupna_imovina = self.components_class_obj.ukupna_imovina(year)

            ratio_results.append(round(float(dugorocne_obaveze / ukupna_imovina), 2))

        ratio_results.reverse()

        return ratio_results

    def gross_profit_margin(self) -> list[float]:
        # """Stopa sposobnosti prihoda da odbacuju poslovni dobitak."""
        ratio_results = []

        for year in range(0, 5):
            poslovni_dobitak = self.components_class_obj.poslovni_dobitak(year)
            prihodi_od_prodaje = self.components_class_obj.prihod_od_prodaje(year)

            ratio_results.append(round(float(poslovni_dobitak / prihodi_od_prodaje), 2))

        ratio_results.reverse()

        return ratio_results

    def net_profit_margin(self) -> list[float]:
        """Racio pokazuje neto prinosnu snagu prihoda 
        od prodaje.
        """
        ratio_results = []

        for year in range(0, 5):
            neto_dobit = self.components_class_obj.neto_dobit(year)
            prihodi_od_prodaje = prihodi_od_prodaje = self.components_class_obj.prihod_od_prodaje(year)

            ratio_results.append(round(float(neto_dobit / prihodi_od_prodaje), 2))

        ratio_results.reverse()

        return ratio_results
    
    def capitalisation_ratio(self) -> list[float]:
        """Pokazuje učešće pozajmljenog kapitala u ukupnom kapitalu. 
        Pokazatelj veći od 1, znači da se preduzeće prezaduženo. 
        Pokazatelj između 0 i 0,5 znači da se sredstva pretežno finansiraju 
        iz sopostvenih kapitala, a pokazatelj između 0,5 i 1 označava 
        povećano finansiranje iz pozajmljenog kapitala.
        """
        ratio_results = []

        for year in range(0, 5):
            obaveze_bez_rezervisanja = self.components_class_obj.obaveze_bez_rezervisanja(year)
            measure_2 = self.components_class_obj._get_aop_value('0420', year) + self.components_class_obj._get_aop_value('0431', year) + self.components_class_obj._get_aop_value('0401', year) - self.components_class_obj._get_aop_value('0403', year) - self.components_class_obj._get_aop_value('0455', year)
            ratio_results.append(round(float(obaveze_bez_rezervisanja / measure_2), 2))

        ratio_results.reverse()

        return ratio_results

    def return_on_bussines_assets(self) -> list[float]:
        """Stopa bruto prinosa na poslovnu imovinu 
        (bez dugoročnih i kratkoročnih plasmana)."""

        ratio_results = []

        for year in range(0, 5):
            poslovna_dobit = self.components_class_obj.poslovni_dobitak(year)
            poslovna_imovina = self.components_class_obj.poslovna_imovina(year)
            ratio_results.append(round(float(poslovna_dobit / poslovna_imovina), 2))

        ratio_results.reverse()

        return ratio_results

    def return_on_assets(self) -> list[float]:
        """Indikator profitabilnosti preduzeća u odnosu na ukupnu imovinu."""

        ratio_results = []

        for year in range(0, 5):
            neto_dobit = self.components_class_obj.neto_dobit(year)
            prihodi_od_prodaje = self.components_class_obj.prihod_od_prodaje(year)
            ratio_results.append(round(float(neto_dobit / prihodi_od_prodaje), 2))

        ratio_results.reverse()

        return ratio_results

    def return_on_equity(self) -> list[float]:
        """Mera profitabilnosti preduzeća u odnosu na sopstveni kapital."""

        ratio_results = []

        for year in range(0, 5):
            neto_dobit = self.components_class_obj.neto_dobit(year)
            kapital = self.components_class_obj.kapital(year)
            ratio_results.append(round(float(neto_dobit / kapital), 2))

        ratio_results.reverse()

        return ratio_results

    def debt_to_equity(self) -> list[float]:
        """Pokazuje kvotu pozajmljenog kapitala u odnosu na sopstveni kapital. 
        Pokazatelj manji od 1, znači da se sredstva finansiraju sopstvenim kapitalom, 
        a pokazatelj iznad 1, označava povećano finansiranje iz pozajmljenog kapitala.
        """
        ratio_results = []

        for year in range(0, 5):
            measure_1 = self.components_class_obj._get_aop_value('0420', year) + self.components_class_obj._get_aop_value('0431', year)
            measure_2 = self.components_class_obj._get_aop_value('0401', year) - self.components_class_obj._get_aop_value('0403', year)  + self.components_class_obj._get_aop_value('0455', year)
            ratio_results.append(round(float(measure_1 / measure_2), 2))

        ratio_results.reverse()

        return ratio_results

    def long_term_financial_stability(self) -> list[float]:
        """Pokazuje pokrivenost dugoročno vezane imovine 
        dugoronim izvorima, što je pokazatelj udaljeniji 
        od "1" prema "0", pokazatelj je bolji.
        """
        ratio_results = []

        for year in range(0, 5):
            measure_1 = self.components_class_obj._get_aop_value('0002', year) + self.components_class_obj._get_aop_value('0031', year)
            measure_2 = self.components_class_obj._get_aop_value('0401', year) - self.components_class_obj._get_aop_value('0403', year) - self.components_class_obj._get_aop_value('0455', year) + self.components_class_obj._get_aop_value('0415', year)

            ratio_results.append(round(float(measure_1 / measure_2), 2))

        ratio_results.reverse()

        return ratio_results

    def EBITDA_margin(self) -> list[float]:

        ratio_results = []

        for year in range(0, 5):
            ebitda = self.components_class_obj.ebitda(year)        
            prihodi_od_prodaje = prihodi_od_prodaje = self.components_class_obj.prihod_od_prodaje(year)

            ratio_results.append(round(float(ebitda / prihodi_od_prodaje), 2))

        ratio_results.reverse()

        return ratio_results

    def broj_zaposlenih(self) -> list[int]:
        """Mera sposobnosti preduzeća da ostvaruje
        dobitak iz poslovnih aktivnosti.
        """
        ratio_results = []

        for year in range(0, 5):
            broj_zaposlenih = self.components_class_obj.broj_zaposlenih(year)

            ratio_results.append(round(int(broj_zaposlenih), 2))

        ratio_results.reverse()

        return ratio_results

    def inventory_turnover(self) -> list[float]:
        """Pokazuje koliko puta se obrnu ukupne zalihe u toku godine - efikasnost 
        ukupnih zaliha.
        """
        ratio_results = []

        for year in range(0, 4):
            prihod_od_prodaje = self.components_class_obj.prihod_od_prodaje(year)
            prosecne_zalihe = self.components_class_obj.prosecne_zalihe(year)
            ratio_results.append(round(float(prihod_od_prodaje/prosecne_zalihe), 2))

        ratio_results.reverse()

        return ratio_results

    def goods_turnover(self) -> list[float]:
        """Pokazuje koliko puta se obrnu zalihe robe u toku godine  - efikasnost 
        zalihama robe. Dani vezivanja = 365/KO. 
        """
        ratio_results = []

        for year in range(0, 4):
            nabavna_vrednost_prodate_robe = self.components_class_obj.nabavna_vrednost_prodate_robe(year)
            prosecne_zalihe_robe = self.components_class_obj.prosecne_zalihe_robe(year)
            ratio_results.append(round(float(nabavna_vrednost_prodate_robe/prosecne_zalihe_robe), 2))

        ratio_results.reverse()

        return ratio_results

    def account_receivable_turnover(self) -> list[float]:
        """Obrt - efikasnost imovine u potraživanja od kupaca. Dani 
        vezivanja = 365/KO. 
        """
        ratio_results = []

        for year in range(0, 4):
            prodaja = self.components_class_obj.prodaja(year)
            prosecni_kupci = self.components_class_obj.prosecni_kupci(year)
            ratio_results.append(round(float(prodaja/prosecni_kupci), 2))

        ratio_results.reverse()

        return ratio_results


