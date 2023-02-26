
from pkg_resources import resource_filename
from datetime import datetime
from threading import Thread
from time import sleep
import customtkinter
import subprocess
import tkinter
import psutil
import shutil
import config
import os



##### * SE CERTIFICA QUE A PASTA PRINCIPAL DE SOFTERS VAI REALMENTE ESTAR CRIADA
try:    os.makedirs(f'{config.dir_install}')
except: pass



##############################################################################
##### * DEFINIÇÃO DAS FUNÇÕES
##############################################################################

lista_pids_filhos = []
def get_pids():
    global lista_pids_filhos
    pid_principal = os.getpid()
    cadeia_de_processos = psutil.Process(pid_principal)
    for processo in cadeia_de_processos.children(recursive=True):
        if processo.pid not in lista_pids_filhos: 
            lista_pids_filhos.append(processo.pid)

def reinicializar():
    global lista_pids_filhos
    cont_pid = 0
    total_pid = len(lista_pids_filhos)
    for pid in lista_pids_filhos:
        if cont_pid != total_pid:
            os.system(f'taskkill /pid {str(pid)} /F') 
        cont_pid+=1
    lista_pids_filhos   = []

def remove_olds():
    '''Remove versões anteriores do softer caso seja desejado'''

    ##### * TENTA APAGAR OS ATALHOS DOS SOFTERS ANTERIORES DA AREA DE TRABALHO
    registrando('Procurando atalhos na área de trabalho para apagar...')
    try:    path_desk = str(os.environ['ONEDRIVE'])+'\\Área de Trabalho\\'
    except: path_desk = None
    if path_desk != None: os.system(f'del "{path_desk}{config.softer_name}_*.lnk"')

    username = str(os.getlogin())
    path_desk2 = f'C:/Users/{username}/Desktop/'
    try:os.system(f'del "{path_desk2}{config.softer_name}_*.lnk"')
    except:pass


    # ##### * INICIO DO PROCESSO DE REMOÇÃO DAS PASTAS DE INSTALAÇÃO DOS SOFTERS ANTERIORES
    # path_enterprise_dir = str(config.dir_install).replace('/','\\')                         # * CAMINHO PRINCIPAL DA PASTA DE SOFTERS
    # resp = subprocess.check_output(f"dir {path_enterprise_dir}", shell=True)                # * COMANDO 'DIR' PARA LISTAR TUDO
    # resp_list = str(resp).split('\\n')                                                      # * SEPARA POR LINHA
    # for item in resp_list:                                                                  
    #     if (                                                                                
    #     item.find   ('<DIR>'    )   != -1)      and (                                       
    #     item.find   ('  .\\r'   )   == -1)      and (                                       # * PARA CADA LINHA:
    #     item.find   ('  ..\\r'  )   == -1)      :                                           # * VERIFICA SE É UMA PASTA
    #         dir_name = item.replace('          ','').split('<DIR>')[1].split('\\r')[0]      # * E SE A PASTA POSSUI O NOME DO SOFTER
    #         if dir_name.find(f'{config.softer_name}_')!=-1:                                                                         
    #             os.system(f'rmdir {path_enterprise_dir}{dir_name} /s/q')                    # * EM CASO POSITIVO DELETA A PASTA        
    pass

def make_dir_install():
    try:    
        os.makedirs(f'{config.dir_install}{config.softer_name}_{config.softer_version}')
        registrando('Criado pasta para a instalação')
        return 'ok'
    except: 
        registrando('Erro ao tentar criar a posta para instalação')
        registrando('Caso o problema persista, entre em contato com o desenvolvedor.')
        return 'erro'

def copy_base():
    base = resource_filename(__name__, 'base.zip')
    shutil.unpack_archive(base, f'{config.dir_install}{config.softer_name}_{config.softer_version}')

def copy_desktop_icon():
    try:
        username = str(os.getlogin())

        try:    path_desk = str(os.environ['ONEDRIVE'].replace('\\','/'))+'/Área de Trabalho/'
        except: path_desk  = f'C:/Users/{username}/Desktop/'

        path_desk2 = f'C:/Users/{username}/Desktop/'

        try:    shutil.copy2(f'{config.dir_install}{config.softer_name}_{config.softer_version}/{config.softer_name}_{config.softer_version}.lnk',path_desk )
        except: shutil.copy2(f'{config.dir_install}{config.softer_name}_{config.softer_version}/{config.softer_name}_{config.softer_version}.lnk',path_desk2)
    except: registrando('Erro ao tentar criar o Atalho')

def registrando(texto):
    dtm = datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
    mensagem = f'{dtm} - {texto}'
    txtbox.insert(tkinter.END,f'{mensagem}\n')
    with open (f'c:/Sistemas/Robos/LOG_Install_{config.softer_name}_{config.softer_version}.txt','a') as arquivo:
        print(mensagem,file=arquivo)
    pass

##############################################################################
##### * INICIO DO SCRIPT DE INSTALAÇÃO E FRONTEND
##############################################################################

janela = customtkinter.CTk()
janela.title(f'Instalador {config.softer_name}, Versão: {config.softer_version}')
janela.geometry("700x500")
txtbox = customtkinter.CTkTextbox(master=janela)
txtbox.pack(fill='both',expand=True)

def install_script():

    registrando(f'Iniciando instalação do softer: {config.softer_name}, Versão: {config.softer_version}')
    registrando(f'Removendo versões anteriores do softer: {config.softer_name}')
    remove_olds()
    if make_dir_install() == 'ok':
        copy_base()
    copy_desktop_icon()
    registrando('Finalizado a instalação')
    sft_name_vers = f'{config.softer_name}_{config.softer_version}'    
    destiny = f'c:/Sistemas/Robos/{sft_name_vers}/{sft_name_vers}.exe'
    os.popen(destiny)  
    registrando('Esta janela já pode ser fechada...')
    sleep(5)
    os.system(f'taskkill /im Instalador_{config.softer_name}_{config.softer_version}.exe /f')

    print(f"""
    \n\n\n
    ==============================================================================
    Finalizado a instalação de uma nova versão.
    Caso tenha alguma dificuldade ou dúvida procure o desenvolvedor responsável.
    ==============================================================================
    \n
    ==============================================================================
    Esta janela já pode ser fechada...
    ==============================================================================
    \n\n\n
    """)




Thread(target=install_script).start()


janela.mainloop()

