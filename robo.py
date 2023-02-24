from openpyxl import load_workbook
from datetime import datetime, timedelta
from os import makedirs
import navegador
import urllib
import config
from time import sleep


class Session:

    def __init__(self):
        try: makedirs(config.path_dir)
        except:pass
        self.define_configuracoes()
        self.rotina()
        pass

    def define_configuracoes(self):
        self.modo_navegador     = 'oculto'                                                                 # * CONFIGURAÇÃO PADRÃO: FIREFOX EXECUTA OCULTO
        self.tmp_min   = 5                
        self.tmp_max   = 30        
        self.linha_ini = 2        
        self.linha_fin = 50            
       
        try:                                                                                    # * TENTA LOCALIZAR ARQUIVO DE CONFIGURAÇÃO
            arquivo = open (f'{config.path_dir}/configs','r')                                                      
            leitura = (str(arquivo.read()).replace(' ','')).split('\n')                         # * RETINA OS ESPAÇOS EM BRANCO
            for linha in leitura:                                                               # * VERIFICA LINHA À LINHA SE EXISTE ALGUMA CONFIGURAÇÃO
                linha = linha.split('=')                                    
                try:
                    chave = linha[0]                                        
                    valor = linha[1]
                except:
                    chave = 'erro'
                    valor = 'erro'
                ##### * ABAIXO FICA AS DEFINIÇÕES
                ##### * DAS OPÇÕES DE CONFIGURAÇÕES DESEJADAS   
                if chave == 'visual'    and valor == '1': self.modo_navegador = 'visivel'           # * VERIFICA CONFIGURAÇÃO DO VISUAL DO FIREFOX
                if chave == 'tmp_min'   : self.tmp_min   = int(valor)
                if chave == 'tmp_max'   : self.tmp_max   = int(valor)
                if chave == 'linha_ini' : self.linha_ini = int(valor)
                if chave == 'linha_fin' : self.linha_fin = int(valor)
            arquivo.close()
        except: pass

    def registrando(self, txt, color='BLACK', vida='DIA'):
        """ * Tratativa dos registros gerados manualmente
        # Args:
            * txt  : A mensagem que será enviada ou salva
            * color: Cor que deseja que a a mensagem seja exibida
            * vida : Tempo de vida util que o log deve ser mantido
                    * 'DIA'
                    * 'SEMANA'
                    * 'MES'
                    * 'ANO'
                    * 'ETERNO'
        """
        registro = str(datetime.now().strftime('%Y/%m/%d-%H:%M:%S-'))+str(txt)                  # * FORMATO EM QUE FICARÁ A MENSAGEM
        nome_arquivo_log = config.toScreen_path
        arquivo_log = open(nome_arquivo_log,'a')                                                # * SALVA O LOG LOCALMENTE NA MÁQUINA
        print (registro, file=arquivo_log)                                                      # * 
        arquivo_log.close()                                                                     # * 
        
        registro_dtm = str(datetime.now().strftime('%Y%m%d'))                                   # * 
        nome_arquivo_log2 =f'{config.path_dir}/Log_{config.softer_name}_{registro_dtm}.txt'
        arquivo_log2 = open(nome_arquivo_log2,'a')                                              # * SALVA O LOG LOCALMENTE NA MÁQUINA
        print (registro, file=arquivo_log2)                                                     # * 
        arquivo_log2.close()                                                                    # * 
        pass

    def old(self):
        zap = navegador.Sessao()
        self.registrando('Abrindo navegador')
        zap.iniciar_navegador()
        self.registrando('Acessado WhatsApp')

        arquivo_txt = open('Dados.txt','r',encoding='utf-8')
        leitura_arquivo_txt = arquivo_txt.read()
        lista_arquivo_txt = leitura_arquivo_txt.splitlines()

        qt_linhas = len(lista_arquivo_txt)
        registrando(f'Temos {qt_linhas} mensagens para enviar')
        cont_msg = 1
        for item in lista_arquivo_txt:
            item = item.split(';')
            numero      = item[0]
            pessoa      = item[1]
            mensagem    = item[2]
            texto           = urllib.parse.quote(f"Oi {pessoa}! {mensagem}")
            zap.send_msg(numero,texto)
            registrando(f'Enviado a mensagem {cont_msg}')
            cont_msg = cont_msg +1

    def rotina(self):
        self.registrando('Iniciado rotina')
        zap = navegador.Sessao()
        zap.iniciar_navegador()



        qt_linhas_trabalhar = self.linha_fin-self.linha_ini
        for item in range(qt_linhas_trabalhar+1):
            tempo_linha_ini = datetime.now()
            linha = self.linha_ini+item
            self.arquivo_xlsx = load_workbook(f'{config.path_dir}/Dados.xlsx')
            self.planilha = self.arquivo_xlsx['Contatos']

            telefone    = self.planilha[f'A{linha}'].value
            cliente     = self.planilha[f'B{linha}'].value
            mensagem    = self.planilha[f'C{linha}'].value
            texto       = urllib.parse.quote(f"Oi {cliente}! {mensagem}")

            self.registrando(f'Trabalhando na linha: {linha}     Fone: {telefone},      Nome: {cliente}')
            zap.send_msg(telefone,texto)

            #############################################################
            tempo_linha_fin         = datetime.now()
            tempo_linha_duracao     = tempo_linha_fin-tempo_linha_ini 
            tempo_minimo            = timedelta(seconds=self.tmp_min)
            diferenca_sleep         = tempo_minimo-tempo_linha_duracao 
            float_dif_sleep         = float(str(diferenca_sleep).split(":")[2])
            # tempo_maximo = timedelta(seconds=self.tmp_max)
            if diferenca_sleep > timedelta(seconds=0):
                sleep(float_dif_sleep)
            else: pass
        pass

start = Session()







