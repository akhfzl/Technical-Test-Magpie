from scrape_rajasusu import ScrapRajaSusu
import pandas as pd
import regex as re

class PreprocessingData(ScrapRajaSusu):
    def __init__(self):
        super().__init__()
        self.linksTarget = [
            'product/pediasure-madu-200gr/',
            'product/pediasure-vanila-850-gr/',
            'product/nutrilon-royal-3-vanila-800-gr/'
        ]
    
    def readAsDataframe(self):
        df = self.startScrapping(self.linksTarget)
        df = pd.DataFrame(df)
        return df
    
    def cleanCurrency(self, currency):
        currency = re.sub(r'[^0-9,]', '', currency)
        currency = int(currency.replace(',', ''))
        return currency
    
    def cleanOfCurrencyDF(self, df):
        df['harga_clean'] = df['harga'].apply(lambda x: self.cleanCurrency(x))
        return df
    
    def saveToCSV(self, df):
        return df.to_csv('case_1/output.csv', index=False)