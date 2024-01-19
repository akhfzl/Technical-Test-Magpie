from selenium import webdriver
from scrape_rajasusu import ScrapRajaSusu
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from dotenv import load_dotenv
import os, time, pandas as pd

load_dotenv()

class ScrappingTokoPedia(ScrapRajaSusu):
    def __init__(self):
        super().__init__()
        self.linkTokoPedia = 'https://www.tokopedia.com/'
        self.ObjectOfTokopedia = {
            'Nama Produk': [],
            # 'Harga Asli': [],
            # 'Discount': [],
            'Harga Discount': [],
            'Jumlah Penjualan': [],
            'Halaman': []
        }
        self.resultScrapBlock = []
        self.wait = WebDriverWait(self.driver, 10)

    def redirectToLinkTokopedia(self):
        return self.driver.get(self.linkTokoPedia)
    
    def enterButtonTokopedia(self, elemenHTML, className):
        # email_login = self.wait.until(EC.presence_of_element_located((self.objectOfElementHtml[elemenHTML], className))) if you wanna login using email/hp
        googleAccount = self.driver.find_element(self.objectOfElementHtml[elemenHTML], className)
        return googleAccount.send_keys(Keys.ENTER)
    
    def SearchItem(self, **search):
        typing = self.driver.find_element(self.objectOfElementHtml['XPATH'], "//input[@aria-label='Cari di Tokopedia']")
        self.namaTarget = str(search['yourtype'])
        typing.send_keys(str(search['yourtype']))
        typing.send_keys(Keys.ENTER)

        self.halaman = search['halaman'] if search['halaman'] else 1

        if self.halaman > 1:
            self.scrollingWindow()
            time.sleep(15)
            try: 
                checkHalaman = self.driver.find_element(By.XPATH, f"//button[contains(text(),'{self.halaman}')]")
                self.scrollingWindow()
                self.driver.execute_script("arguments[0].click();", checkHalaman)
                return True
            except NoSuchElementException:
                return False
        
        return True
    
    def collectingData(self, elemenHTML, keys):
        myArray = []

        elementProduk = self.wait.until(EC.visibility_of_all_elements_located((self.objectOfElementHtml[elemenHTML[keys]['selector']], elemenHTML[keys]['class_name_1'])))
        self.scrollingWindow(elementProduk)
        # time.sleep(30)
        myArray.extend(elementProduk)

        if keys not in ['Harga Asli', 'Jumlah Penjualan']:
            elementProduk = self.wait.until(EC.presence_of_all_elements_located((self.objectOfElementHtml[elemenHTML[keys]['selector']], elemenHTML[keys]['class_name_1'])))
            self.scrollingWindow(elementProduk)
            # time.sleep(30)
            myArray.extend(elementProduk)

        elementProduk = list(map(lambda x: x.text, myArray))

        self.ObjectOfTokopedia[keys].extend(elementProduk)
        return self.ObjectOfTokopedia
    
    def scrollingWindow(self, item=None):
        if item != None:
            return self.driver.execute_script("arguments[0].scrollIntoView;", item)
        
        return self.driver.execute_script("window.scrollTo(0, 1000);")
    
    def returnAllData(self):
        self.ObjectOfTokopedia['Halaman'] = [self.halaman if self.halaman else 1 for i in range(len(self.ObjectOfTokopedia['Nama Produk']))]
        return self.ObjectOfTokopedia
    
    #new 
    def splitNesChar(self, txt):
        txt = txt.splitlines()
        txt = ';'.join(txt)
        return f'{txt}\n'
    
    def getAllBlock(self, **selector):
        retries = 0
        maxRetries = 5

        while retries <= maxRetries:
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                while True:
                    elements = self.driver.find_elements(self.objectOfElementHtml[selector['byOfChoice']], selector['paternOfSelector'])
                    self.resultScrapBlock.extend(list(map(lambda x: self.splitNesChar(x.text), elements)))  
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(25)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        print('Berhenti karena new_height == last_height')
                        break 
                    last_height = new_height
                
                print('Berhenti karena kondisi bukan True')
                break

            except StaleElementReferenceException or TimeoutException:
                self.driver.refresh()
                retries += 1

        with open(f'case_1/result_scrape_txt/{self.namaTarget}Scrape.txt', 'w') as file:
            file.writelines(self.resultScrapBlock)

        return self.resultScrapBlock
    # new

    def readPandas(self, arrays):
        print('myarrays', arrays)
        print('length Nama Produk', len(arrays['Nama Produk']))
        print('length Nama Produk', len(arrays['Halaman']))
        print('length Nama Produk', len(arrays['Harga Discount']))
        print('length Nama Produk', len(arrays['Jumlah Penjualan']))
        # df = pd.DataFrame(arrays)
        # return df.head()

# call class
# scrap = ScrappingTokoPedia()
# driver = scrap.redirectToLinkTokopedia()
# loginTokped = scrap.SearchItem(yourtype='konichiwa', halaman=1)
# if loginTokped:
#     loginTokped = scrap.getAllBlock(byOfChoice='XPATH', paternOfSelector="//div[@class='css-1asz3by']")
#     print('total:', len(loginTokped), 'example:', loginTokped[0] if len(loginTokped) > 0 else 'tidak ada data')
# else:
#     print('Halaman tidak cukup')
