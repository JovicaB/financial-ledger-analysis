import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


class FinancialDataVisualization:

    @staticmethod
    def aggregate_data_for_comparative_visualization(df_companys_fr: pd.DataFrame, df_competitors_fr: pd.DataFrame, aop_code: str, years: list):
        """
        Aggregates financial data for the company and its competitors for a specific AOP code.

        Args:
            df_companys_fr (pd.DataFrame): Company financial data.
            df_competitors_fr (pd.DataFrame): Competitors' financial data.
            aop_code (str): The AOP code to filter data.

        Returns:
            tuple: (result_company_df, result_competitors_data_df) - Processed dataframes.
        """
        if aop_code not in df_companys_fr['AOP'].values:
            raise ValueError(f"AOP code {aop_code} not found in company dataset.")

        result_company_df_lst = df_companys_fr.loc[df_companys_fr['AOP'] == aop_code].iloc[0, 2:].to_list()
        result_company_df = pd.DataFrame([result_company_df_lst], columns=years)

        competitors_data_lst = df_competitors_fr.loc[df_competitors_fr['AOP'] == aop_code].iloc[0, 2:].to_list()
        competitors_data_lst.append(result_company_df_lst[-1])
        # header = ['competitor_1', 'competitor_2', 'competitor_3', 'competitor_4', 'competitor_5', 'company']
        header = ['konkurent #1', 'konkurent #2', 'konkurent #3', 'konkurent #4', 'konkurent #5', 'kompanija']
        result_competitors_data_df = pd.DataFrame([competitors_data_lst], columns=header)

        return result_company_df, result_competitors_data_df

    @staticmethod
    def comparative_analysis_visualization(df_company: pd.DataFrame, df_competitors: pd.DataFrame, opis: str):
        """
        Creates a comparative line and bar chart of company performance vs competitors.

        Args:
            df_company (pd.DataFrame): Company data for plotting.
            df_competitors (pd.DataFrame): Competitors' data for plotting.
            opis (str): Variable to be analyzed.
        """
        plt.figure(figsize=(16, 4))
        years = [2019, 2020, 2021, 2022, 2023]

        plt.subplot(1, 2, 1)
        plt.plot(years, df_company.loc[0].values, marker='o', color='MediumSeaGreen', label="Kompanija")
        # plt.title(f"Poređenje: {opis} tokom 5 godina", fontsize=10)
        plt.xlabel(opis, fontsize=8)
        plt.ylabel(opis, fontsize=8)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(years)
        plt.legend()

        plt.subplot(1, 2, 2)
        # bar_labels = df_competitors.columns
        bar_labels = ['konkurent #1', 'konkurent #2', 'konkurent #3', 'konkurent #4', 'konkurent #5', 'kompanija']
        bar_values = df_competitors.loc[0]
        bar_colors = ['DarkGray'] * 5 + ['MediumSeaGreen']
        plt.bar(bar_labels, bar_values, color=bar_colors)
        plt.title("Poređenje poslednje godine sa konkurencijom", fontsize=10)
        plt.ylabel(opis, fontsize=8)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.6)

        plt.tight_layout()
        # plt.show()

    @staticmethod
    def comparative_analysis_visualization_with_revenue(df_company_2row: pd.DataFrame, df_competition_2rows: pd.DataFrame, description_main_var: str):  
        """
        Visualizes comparison between company data and competitors, including revenue.

        Args:
            df_company_2row (pd.DataFrame): Company data with two rows.
            df_competition_2rows (pd.DataFrame): Competitors' data with two rows.
            description_main_var (str): Main variable for comparison.
        """
        fig, axes = plt.subplots(1, 2, figsize=(16, 4))
        # fig.suptitle(f"Poređenje: {description_main_var} i prihodi (poslednjih 5 godina poslovanja)", fontsize=16)
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

        bar_labels = ['konkurent #1', 'konkurent #2', 'konkurent #3', 'konkurent #4', 'konkurent #5', 'kompanija']
        df_competition_2rows.index = ["bar_values", "line_values"]
        df_competition_2row_normalized = df_competition_2rows.div(df_competition_2rows.max(axis=1), axis=0)
        bar_colors = ['DarkGray'] * 5 + ['MediumSeaGreen']
        axes[1].bar(df_competition_2row_normalized.columns, df_competition_2row_normalized.loc["line_values"], color=bar_colors, alpha=0.7, label=description_main_var)
        axes[1].plot(df_competition_2row_normalized.columns, df_competition_2row_normalized.loc["bar_values"], marker='o', color='IndianRed', label="prihodi")
        axes[1].set_title(f"Poređenje: {description_main_var} i prihodi (konkurencija)", fontsize=10)
        axes[1].set_xlabel("Godina", fontsize=10)
        axes[1].legend()
        axes[1].grid(axis='y', linestyle='--', alpha=0.6)
        # axes[1].set_xticks(bar_labels)
        axes[1].set_xticks(range(len(bar_labels)))
        axes[1].set_xticklabels(bar_labels, rotation=45)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def barplot_ratio_analysis(company_df, competitors_df, ratio_text: str, last_bar_color='g'):
        """
        Creates two bar charts: one for annual performance comparison and one for comparison with competitors.

        Args:
            company_df (pd.DataFrame): Company performance data.
            competitors_df (pd.DataFrame): Competitors' performance data.
            ratio_text (str): The ratio to be analyzed.
            last_bar_color (str): Color for the last bar (company). Default is 'g' (green).

        Returns:
            None: Displays the generated plots.
        """
        if last_bar_color == 'g':
            last_bar_color = (107/255, 179/255, 139/255, 1)
        elif last_bar_color == 'r':
            last_bar_color = 'IndianRed'
        else:
            ValueError("Use 'g' or 'r' only")

        fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
        # fig.suptitle(f"Poređenje: {ratio_text} tokom 5 godina", fontsize=16)
        # Left plot
        sb.barplot(x=company_df.columns, y=company_df.iloc[0], ax=axes[0], color=(133/255, 145/255, 155/255, 1))
        axes[0].set_title(f'Petogodišnji {ratio_text}', fontsize=10)
        axes[0].set_xlabel('Godina', fontsize=9)
        axes[0].set_ylabel(ratio_text, fontsize=9)

        # Right plot
        sb.barplot(x=competitors_df.columns, y=competitors_df.iloc[0], ax=axes[1], color='Silver')
        company_value = competitors_df['company'].iloc[0]

        for patch in axes[1].patches:
            if patch.get_x() == competitors_df.columns.get_loc('company') - 0.4: 
                patch.set_facecolor(last_bar_color)
        
        bar_labels = ['konkurent #1', 'konkurent #2', 'konkurent #3', 'konkurent #4', 'konkurent #5', 'kompanija']
        axes[1].set_title(f"{ratio_text} poređenje sa konkurencijom", fontsize=10)
        axes[1].set_xlabel('Konkurencija / kompanija', fontsize=9)
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].set_ylabel(ratio_text, fontsize=9)
        axes[1].set_xticks(range(len(bar_labels)))
        axes[1].set_xticklabels(bar_labels, rotation=45)

        plt.tight_layout()
        plt.show()
