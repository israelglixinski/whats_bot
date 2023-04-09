from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

        try: 
            self.navegador.find_element(By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div/div/div').click()
            retorno = 'nu_invalido'
        except:
            try: no_nu_contact = self.navegador.find_element(By.XPATH,'//*[@id="main"]/header/div[2]/div/div/span').get_attribute('innerHTML')
            except:
                try: no_nu_contact = self.navegador.find_element(By.XPATH,'/html/body/div[1]/div/div/div[4]/div/header/div[2]/div/div/span').get_attribute('innerHTML')
                except:
                    try: no_nu_contact = self.navegador.find_element(By.CSS_SELECTOR,'._21nHd > span:nth-child(1)').get_attribute('innerHTML')
                    except: no_nu_contact = 'erro_contato'
            

            # if no_nu_contact =='erro_contato':
            #     retorno = no_nu_contact
            # else:
            if True:

                if (str(no_nu_contact)[-4:] == str(numero)[-4:]) or (no_nu_contact =='erro_contato'): 
                
                    enviar = 'sim'

                    lista_xpath = [

                    '//*[@id="main"]/div[2]/div/div[2]/div[2]/div[10]/div/div/div[1]/div[1]/div[1]/div/span[1]/span'
                    ,'//*[@id="main"]/div[2]/div/div[2]/div[2]/div[9]/div/div/div[1]/div[1]/div[1]/div/span[1]/span'
                    ,'//*[@id="main"]/div[2]/div/div[2]/div[2]/div[8]/div/div/div[1]/div[1]/div[1]/div/span[1]/span'
                    ,'//*[@id="main"]/div[2]/div/div[2]/div[3]/div[2]/div/div/div[1]/div[1]/div/div[2]/div'
                    ,'//*[@id="main"]/div[2]/div/div[2]/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div'
                    ,'//*[@id="main"]/div[2]/div/div[2]/div[3]/div[2]/div/div/div[1]/span[2]'
                    ,'//*[@id="main"]/div[2]/div/div[2]/div[3]/div[3]/div/div/div[1]/div[1]'
                    ]
                    
                    for xpht in lista_xpath:
                        try:
                            history = self.navegador.find_element(By.XPATH,xpht).get_attribute('innerHTML')
                            print(history)
                            enviar = 'nao'
                        except: pass

                    if enviar == 'sim':
                       
                        
                        try: self.navegador.find_element(By.XPATH,'/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(Keys.ENTER)
                        except:
                            try: self.navegador.find_element(By.XPATH,'/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p').send_keys(Keys.ENTER)
                            except:
                                try: self.navegador.find_element(By.XPATH,'/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]').click()
                                except: self.navegador.find_element(By.CSS_SELECTOR,'button.tvf2evcx > span:nth-child(1)').click()
                        
                       
                        # self.navegador.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
                        # self.navegador.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
                       
                       
                       
                       
                        retorno = 'enviado'
                    else:
                        retorno = 'tem_msg'

                else:
                    retorno = 'nu_salvo'

        sleep(10)



        return retorno


 




