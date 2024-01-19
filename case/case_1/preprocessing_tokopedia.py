from scrape_tokopedia import ScrappingTokoPedia
import pathlib, regex as re, pandas as pd

class PreprocessingTokopedia:
    def __init__(self):
        self.folder = 'case_1/result_scrape_txt'
        self.save_to_excel = 'case_1/result_excel'
        self.listOfFile = list(pathlib.Path(self.folder).glob('*'))
        self.wordNotImportand = [
            r'^Terlaris', 
            r'^Promo Rockbros',
            r'^Tokopedia Sports',
            r'^Sisa',
            r'^Spesial Untukmu',
            r'^Serbu OS'
        ]
    
    def startScraping(self, yourtype, halaman):
        scrap = ScrappingTokoPedia()
        loginTokped = scrap.redirectToLinkTokopedia()
        loginTokped = scrap.SearchItem(yourtype=yourtype, halaman=halaman)
        if loginTokped:
            loginTokped = scrap.getAllBlock(byOfChoice='XPATH', paternOfSelector="//div[@class='css-1asz3by']")
            print('total:', len(loginTokped), 'example:', loginTokped[0] if len(loginTokped) > 0 else 'tidak ada data')
        else:
            print('Halaman tidak cukup')
    
    def readFiles(self, indexFile):
        getFile = str(self.listOfFile[indexFile]).split('\\')
        getFile = getFile[len(getFile) - 1].split('.')
        self.filename = getFile[0]

        with open(self.listOfFile[indexFile], 'r') as file:
            myFile = file.readlines()
       
        return myFile
    
    def removingTextNotImportant(self, myArray):
        arrayExtend = []
        for arrays in myArray:
            letSplit = arrays.split(';')
            letSplit = [array for array in letSplit if not any(re.match(pattern, array) for pattern in self.wordNotImportand)]
            letSplit = ';'.join(letSplit)
            arrayExtend.append(letSplit)

        return arrayExtend
    
    def spreadTheTextNeeded(self, myArray):
        arrIndex = 0
        mArray = []
        while arrIndex < len(myArray):
            mObject = {}
            letSplit = myArray[arrIndex].split(';')
            
            mObject['Nama SKU'] = letSplit[0]
            mObject['Jumlah Penjualan'] = next((val for val in letSplit if re.compile(r'terjual').search(val)), None)
            mObject['Harga Penjualan'] = next((val for val in letSplit if re.compile(r'Rp').search(val)), None)
            mArray.append(mObject)
            arrIndex += 1
        
        return mArray
    
    def searchNumberOnly(self, text):
        pattern = re.compile(r'\b(\d+)\b')
        if text:
            match = pattern.search(text)
            if match: 
                return int(match.group(1))
            else:
                secPattern = re.compile(r'(\d+)')
                secMatch = secPattern.search(text)
                return int(secMatch.group(1))
            
        return 0
    
    def cleanCurrency(self, currency):
        currency = re.sub(r'[^0-9,]', '', currency)
        currency = int(currency.replace(',', ''))
        return currency

    def readPandas(self, mArray):
        df = pd.DataFrame(mArray)
        df['Jumlah Penjualan'] = df['Jumlah Penjualan'].apply(lambda val: self.searchNumberOnly(val))
        df['Harga Penjualan'] = df['Harga Penjualan'].apply(lambda val: self.cleanCurrency(val))
        df['Estimasi GMV'] = df['Harga Penjualan'] * df['Jumlah Penjualan'] 
        df['Number Of Page'] = 5 if self.filename == 'matoaScrape' else 1

        df.to_csv(f'{self.save_to_excel}/{self.filename}.csv', sep=';',index=False)

        return df

    def mergeSeveralData(self, arrDf):
        df= pd.concat(arrDf, ignore_index=True)
        df.to_csv(f'{self.save_to_excel}/finalResult.csv', index=False)
        return df.head()
                
