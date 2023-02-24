from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import os
import config

class Sessao:

    def __init__(self):


        # self.path_current        = os.getcwd()
        # self.path_bot_data       = f'{self.path_current}\\bot_data'
        self.path_save_chrome    = f'{config.path_dir}\\save_chrome'
        try: os.makedirs(self.path_save_chrome)
        except: pass
        self.chrome_options = Options()
        self.chrome_options.add_argument(f"user-data-dir={self.path_save_chrome}")
        # self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument(f"--log-level=3")
        pass

    def iniciar_navegador(self):
        self.navegador = webdriver.Chrome(chrome_options=self.chrome_options)
        self.navegador.get("https://web.whatsapp.com/")
        while len(self.navegador.find_elements(By.ID,"side")) < 1: sleep(1)

    def try_wait(self,tentativa=1):
        if tentativa < 20:
            sleep(2)
            try:
                while len(self.navegador.find_elements(By.ID,"side")) < 1: sleep(1)
                sleep(1)
            except:
                tentativa = tentativa + 1
                self.try_wait(tentativa)
        pass
        
    def send_msg(self,numero,texto):
        self.chrome_options.add_argument("--headless")
        link    = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
        self.navegador.get(link)
        self.try_wait()
        self.navegador.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
        sleep(10)



 




