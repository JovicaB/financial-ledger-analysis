from typing import Type

import pandas as pd

from components import ComponentsFR


class RatioAnalysis:
    def __init__(self, data: pd.DataFrame, fr_component_obj: Type[object]):
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
            obrtna_imovina = self.components_class_obj.obrtna_imovina(year)
            zalihe = self.components_class_obj.zalihe(year)
            kratkorocne_obaveze = self.components_class_obj.kratkorocne_obaveze(year)

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


from components import ComponentsFR
components_obj = 2