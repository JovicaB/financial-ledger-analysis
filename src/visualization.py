import pandas as pd
import matplotlib.pyplot as plt

class FinancialDataVisualization:

    @staticmethod
    def aggregate_data_for_comparative_visualization(df_companys_fr: pd.DataFrame, df_competitors_fr: pd.DataFrame, aop_code: str):
        """
        Processes financial report (FR) data for a specific AOP (financial position reg.number) code, 
        generating separate datasets for the company's financial results and those of its competitors.

        Args:
            df_companys_fr (pd.DataFrame)
            df_competitors_fr (pd.DataFrame)
            aop_code (str)

        Returns:
            tuple: A tuple containing:
                - result_company_df (pd.DataFrame): DataFrame with a single row representing the company's financial data 
                across the years 2019 to 2023.
                - result_competitors_data_df (pd.DataFrame): DataFrame with a single row containing financial data for 
                competitors and the company for the same period.
        years = [2019, 2020, 2021, 2022, 2023]
        """
        if aop_code not in df_companys_fr['AOP'].values:
            raise ValueError(f"AOP code {aop_code} not found in company dataset.")
        result_company_df_lst = df_companys_fr.loc[df_companys_fr['AOP'] == aop_code, years].iloc[0].to_list()
        result_company_df = pd.DataFrame([result_company_df_lst], columns=years)
        competitors_data_lst = df_competitors_fr.loc[df_competitors_fr['AOP'] == aop_code].iloc[0, 2:].to_list()
        competitors_data_lst.append(result_company_df_lst[-1])
        header = ['competitor_1', 'competitor_2', 'competitor_3', 'competitor_4', 'competitor_5', 'company']
        result_competitors_data_df = pd.DataFrame([competitors_data_lst], columns=header)

        return result_company_df, result_competitors_data_df

    @staticmethod
    def comparative_analysis_visualization(df_company: pd.DataFrame, df_competitors: pd.DataFrame, opis: str):
        plt.figure(figsize=(10, 4))
        years = [2019, 2020, 2021, 2022, 2023]

        plt.subplot(1, 2, 1)
        plt.plot(years, df_company.loc[0].values, marker='o', color='MediumSeaGreen', label="Kompanija")
        plt.title(f"Poređenje: {opis} tokom 5 godina", fontsize=10)
        plt.xlabel(opis, fontsize=8)
        plt.ylabel(opis, fontsize=8)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(years)
        plt.legend()

        plt.subplot(1, 2, 2)
        bar_labels = df_competitors.columns
        bar_values = df_competitors.loc[0]
        bar_colors = ['DarkGray'] * 5 + ['MediumSeaGreen']
        plt.bar(bar_labels, bar_values, color=bar_colors)
        plt.title("Poređenje poslednje godine sa konkurencijom", fontsize=10)
        plt.ylabel(opis, fontsize=8)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def comparative_analysis_visualization_with_revenue(df_company_2row: pd.DataFrame, df_competition_2rows: pd.DataFrame, description_main_var: str):  
        fig, axes = plt.subplots(1, 2, figsize=(16, 4))
        df_company_2row.index = ["bar_values", "line_values"]

        df_company_2row_normalized = df_company_2row.div(df_company_2row.max(axis=1), axis=0)
        axes[0].bar(df_company_2row_normalized.columns, df_company_2row_normalized.loc["bar_values"], color='CadetBlue', alpha=0.7, label=description_main_var)
        axes[0].plot(df_company_2row_normalized.columns, df_company_2row_normalized.loc["line_values"], marker='o', color='IndianRed', label="prihodi")
        axes[0].set_title(f"Poređenje: {description_main_var} i prihodi (poslednjih 5 godina poslovanja)", fontsize=10)
        axes[0].set_xlabel("Godina", fontsize=10)
        axes[0].set_ylabel("Relativna vrednost", fontsize=10)
        axes[0].legend()
        axes[0].grid(axis='y', linestyle='--', alpha=0.6)
        axes[0].set_xticks(df_company_2row_normalized.columns)

        df_competition_2row_normalized = df_company_2row.div(df_company_2row.max(axis=1), axis=0)
        axes[1].bar(df_competition_2row_normalized.columns, df_competition_2row_normalized.loc["line_values"], color='DarkGrey', alpha=0.7, label=description_main_var)
        axes[1].plot(df_competition_2row_normalized.columns, df_competition_2row_normalized.loc["bar_values"], marker='o', color='IndianRed', label="prihodi")
        axes[1].set_title(f"Poređenje: {description_main_var} i prihodi (konkurencija)", fontsize=10)
        axes[1].set_xlabel("Godina", fontsize=10)
        axes[1].legend()
        axes[1].grid(axis='y', linestyle='--', alpha=0.6)
        axes[1].set_xticks(df_competition_2row_normalized.columns)

        plt.tight_layout()
        plt.show()