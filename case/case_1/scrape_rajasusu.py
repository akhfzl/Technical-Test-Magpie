from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 

class ScrapRajaSusu:
    def __init__(self):
        self.driverPath = '../tools/chromedriver.exe'
        self.link = 'https://rajasusu.com'
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument('--headless')
        self.options.add_argument('window-size=1200x600')
        self.options.add_experimental_option('useAutomationExtension', True)
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options=self.options)
        self.objectOfElementHtml = {
            'ID': By.ID,
            'XPATH': By.XPATH,
            'LINK_TEXT': By.LINK_TEXT,
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
            'NAME': By.NAME,
            'TAG_NAME': By.TAG_NAME,
            'CLASS_NAME': By.CLASS_NAME,
            'CSS_SELECTOR': By.CSS_SELECTOR
        }

        self.ObjectDataframe = {
            'Nama SKU': [],
            'harga': [],
            'halaman': []
        }
        
    
    def redirectToLink(self, slashURL):
        # wait = WebDriverWait(self.driver, 10)
        # return wait
        self.driver.get(f'{self.link}/{slashURL}') 
        return self.driver

    def getElement(self, elemenHTML, nameSelector, driver):
        element = driver.find_element(self.objectOfElementHtml[elemenHTML], nameSelector)
        return element.text

    def startScrapping(self, targets): 
        for linkTarget in targets:
            driver = self.redirectToLink(linkTarget)
            sku_element = self.getElement('CLASS_NAME', 'sku', driver)
            harga_element = self.getElement('TAG_NAME', 'bdi', driver)
            halaman_element = linkTarget
            self.ObjectDataframe['Nama SKU'].append(sku_element)
            self.ObjectDataframe['harga'].append(harga_element)
            self.ObjectDataframe['halaman'].append(halaman_element)

        return self.ObjectDataframe

