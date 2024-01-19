from preprocessing_rajasusu import PreprocessingData
from preprocessing_tokopedia import PreprocessingTokopedia
import os

if __name__ == '__main__':
    selectWannaScrap = input(str('What do you want ? Tokopedia/Rajasusu: '))
    if selectWannaScrap == 'Rajasusu':
        process = PreprocessingData()
        df = process.readAsDataframe()
        df = process.cleanOfCurrencyDF(df)
        process.saveToCSV(df)
    
    else:
        tasks = [
            {
                'keyword': 'Rockbros',
                'number_of_page': 1
            },
            {
                'keyword': 'Matoa',
                'number_of_page': 5
            },
            {
                'keyword': 'konichiwa',
                'number_of_page': 10
            }
        ]

        resultScraping = os.listdir('case_1/result_scrape_txt')
        dfArray = []

        letStartPreprocess = PreprocessingTokopedia()

        for i in range(len(resultScraping)):
            # scrapping process
            # arrayFile = letStartPreprocess.startScraping(tasks[i]['keyword'], tasks[i]['number_of_page'])

            # post-process data
            arrayFile = letStartPreprocess.readFiles(i)
            arrayFile = letStartPreprocess.removingTextNotImportant(arrayFile)
            arrayFile = letStartPreprocess.spreadTheTextNeeded(arrayFile)
            arrayFile = letStartPreprocess.readPandas(arrayFile)
            dfArray.append(arrayFile)
        
        # read using pandas and merge multiple dataframe
        arrayFile = letStartPreprocess.mergeSeveralData(dfArray)
        print(arrayFile)
