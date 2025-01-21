from cryptography.fernet import Fernet 
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep
import urllib3
import config
import psutil
import os
import banco
import base64
import subprocess

class Ferramentas:
    def salva_teste(nome_teste,resultado):
        """ # Salva um arquivo de teste com o resultado obtido
        """
        arquivo = open(f'x_{nome_teste}','w')
        print (resultado, file=arquivo)
        arquivo.close()

    def localiza_javax(codigo):
        """ # Procura a variável 'javax.faces.ViewState' na resposta do request e já define o novo valor na variável global
        """
        global javax_faces_ViewState # * VARIAVEL QUE RECEBERÁ O NUMERO DA SESSÃO DO ATENDER2
        search_lines = str(codigo).split('\n')
        for line in search_lines:   
            check_line                  =   line.find('j_id1:javax.faces.ViewState:')
            if check_line               !=  (-1):
                filter_one              =   line.split(' value="')
                filter_two              =   filter_one[1].split('"')
                javax_faces_ViewState   =   filter_two[0]
        return javax_faces_ViewState        

    def encrypta_fernet(senha):
        key = b'N-nMdHttV7-iyB_FxR9Q5NlfkEd1QGp12iVfn-RPEZY='
        f = Fernet(key)
        enc = f.encrypt(senha.encode())
        enc = str(str(enc).replace("b'", "")).replace("'",'')
        return enc

class ignition:

    def __init__(self,feedback, janela, senha, action):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.feedback               = feedback  
        self.janela                 = janela
        self.usuario                = os.getlogin()
        self.senha                  = senha
        self.lista_pids_filhos      = []
        self.crypto_pass            = None
        if action == "verifica": self.verifica_senha_sigal  ()
        if action == "atualiza": self.atualizador           ()
        if action == "start_bot": self.gerencia           ()
        pass

    def registrando(self, texto, color='BLACK', vida='SEMANA'):
        dtm_reg = str(datetime.now().strftime('%Y/%m/%d-%H:%M:%S'))
        mensagem = f'{dtm_reg}-{texto}'
        self.feedback.put([mensagem])
        pass

    def my_decoder_64(self,file_name_with_ext,encoded_string):
        new_file = base64.b64decode(encoded_string)
        with open(file_name_with_ext, "wb") as img_file:
            img_file.write(new_file)

    def atualizador(self):
        self.feedback.put(['...',None,'bloquear'])
        self.registrando('Fazendo download da nova versão...')
        new_top = banco.Robo.Versionamento.download_top_version()[0]
        new_version = f'{new_top[0]}.{new_top[1]}.{new_top[2]}'
        destiny = f'c:/Sistemas/Robos/Instalador_{config.softer_name}_{new_version}.exe'
        with open(destiny, "wb") as img_file: img_file.write(base64.b64decode(new_top[3]))
        self.registrando('Download concluído')
        os.popen(destiny)        
        self.registrando('Fecharei esta tela, e continuarei a instalação em outra janela...')
        os.system(f'taskkill /im {config.softer_name}_{config.softer_version}.exe /f')
        sleep(5)

    def reinicializar(self):
        cont_pid = 0
        for pid in self.lista_pids_filhos:
            if cont_pid != 0:
                # os.system(f'taskkill /pid {str(pid)} /F') 
                subprocess.Popen(f'taskkill /pid {str(pid)} /F', shell=True)
            cont_pid+=1
        self.lista_pids_filhos   = []
        os.popen(f'{config.dir_install}{config.softer_name}_{config.softer_version}/{config.script_robo}.exe')

    def get_pids(self):
        pid_principal = os.getpid()
        primeiro_nivel = psutil.Process(pid_principal)
        for processo in primeiro_nivel.children(recursive=True):
            if processo.pid not in self.lista_pids_filhos: 
                self.lista_pids_filhos.append(processo.pid)

    def define_configuracoes(self):
        self.modo_navegador     = 'oculto'                                                                 # * CONFIGURAÇÃO PADRÃO: FIREFOX EXECUTA OCULTO
        self.tmp_min   = 5                
        self.tmp_max   = 90        
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

    def gerencia(self):
        self.feedback.put(['...',None,'bloquear'])
        self.define_configuracoes()

        self.get_pids()
        self.registrando('Iniciando o Robô pela primeira vez...')
        os.popen(f'{config.dir_install}{config.softer_name}_{config.softer_version}/{config.script_robo}.exe')
        registro_dtm = str(datetime.now().strftime('%Y%m%d')) 
        logfile = f'{config.dir_install}{config.softer_name}_{config.softer_version}/Log_{config.softer_name}_{registro_dtm}.txt'

        try:    sizeLog = Path(logfile).stat().st_size
        except: sizeLog = 0

        try:    self.win_alive = self.janela.state()
        except: self.win_alive = 'Finalizado'

        loop_time = timedelta(seconds=self.tmp_max)
        self.prox_exec = datetime.now() + loop_time

        self.front_alive_0 = True
        alter_front_alive = datetime.fromtimestamp(Path(config.front_alive_path).stat().st_mtime)
        if alter_front_alive < (datetime.now() - timedelta(seconds=2)): self.front_alive_0 = False
        
        while self.front_alive_0 == True:
            
            self.get_pids()
            if self.prox_exec < datetime.now():
               
                registro_dtm = str(datetime.now().strftime('%Y%m%d')) 
                logfile = f'{config.dir_install}{config.softer_name}_{config.softer_version}/Log_{config.softer_name}_{registro_dtm}.txt'
                try:    newSizeLog = Path(logfile).stat().st_size
                except: newSizeLog = 0

                if newSizeLog == sizeLog:
                    self.registrando('Reiniciando processo de automatização')
                    self.reinicializar()

                try:    sizeLog = Path(logfile).stat().st_size
                except: sizeLog = 0
                self.registrando('...')

                self.prox_exec = datetime.now() + loop_time

            alter_front_alive = datetime.fromtimestamp(Path(config.front_alive_path).stat().st_mtime)
            if alter_front_alive < (datetime.now() - timedelta(seconds=2)): self.front_alive_0 = False            

            sleep(1)

    def start_bot(self):
        self.feedback.put(['...',None,'bloquear'])
        self.registrando('Iniciando o Robô...')
        os.popen(f'{config.dir_install}{config.softer_name}_{config.softer_version}/{config.script_robo}.exe')
        sleep(5)

        self.feedback.put(['...',None,'desbloquear'])
