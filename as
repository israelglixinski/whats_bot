
from datetime import datetime, timedelta 
from cryptography.fernet import Fernet   
from Crypto.Cipher import AES            
from threading import Thread             
from pathlib import Path
from time import sleep                   
from glob import glob                    
import subprocess
import binascii                          
import config
import base64                            
import psutil
import banco                             
import sigal                             
import json                              
import sys                               
import os                                

class automacao:
    ''' * Classe principal responsável pela a aplicação do robô'''
    
    def __init__(self):
        ''' * Inicializador'''
        self.define_configuracoes()                                                             # * VERIFICA SE FOI PASSADA ALGUMA CONFIGURAÇÃO PELO USUÁRIO
        self.idContratoGestor       = None
        self.cont_feedback          = False
        self.front_alive            = True
        
        try:


            ######################################
            # userstring_test = 'gAAAAABj9lLP_MXiQGAfYwjJypFiNRaMNJwsjz0sfF5Q2QY_lVEIVnI8z-pGVP2CK1HkhyKAjTCHdolhPVgQDlwycNjwnwoUETxlelaFIoDwxwwXdJMLESc='
            # credenciais = str(self.decrypta_fernet(userstring_test.encode('ascii'))).split('*%@%*')
            ######################################

            credenciais = str(self.decrypta_fernet(sys.argv[1].encode('ascii'))).split('*%@%*')
            self.matGestor      = credenciais[0]
            self.senhaGestor    = credenciais[1]
        except:
            self.matGestor      = 'Zero'
            self.senhaGestor    = 'Zero'

        Thread(target               = self.check_alive).start()
        Thread(target               = self.controle_de_acoes).start()                           # * EXECUTA A ROTINA PRINCIPAL DENTRO DE UMA CAMADA DE THREAD

    def define_configuracoes(self):
        self.modo_navegador     = 'oculto'                                                                 # * CONFIGURAÇÃO PADRÃO: FIREFOX EXECUTA OCULTO
        self.cfg_reset          = 'ativo'                                                                 # * CONFIGURAÇÃO PADRÃO: FIREFOX EXECUTA OCULTO
        self.cfg_cadastro       = 'ativo'                                                                 # * CONFIGURAÇÃO PADRÃO: FIREFOX EXECUTA OCULTO
        self.cfg_acesso         = 'ativo'                                                                 # * CONFIGURAÇÃO PADRÃO: FIREFOX EXECUTA OCULTO
        self.cfg_remocao        = 'ativo'                                                                 # * CONFIGURAÇÃO PADRÃO: FIREFOX EXECUTA OCULTO
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
                if chave == 'reset'     and valor == '0': self.cfg_reset      = 'desativado'        # * VERIFICA CONFIGURAÇÃO DO VISUAL DO FIREFOX
                if chave == 'cadastro'  and valor == '0': self.cfg_cadastro   = 'desativado'        # * VERIFICA CONFIGURAÇÃO DO VISUAL DO FIREFOX
                if chave == 'acesso'    and valor == '0': self.cfg_acesso     = 'desativado'        # * VERIFICA CONFIGURAÇÃO DO VISUAL DO FIREFOX
                if chave == 'remocao'   and valor == '0': self.cfg_remocao    = 'desativado'        # * VERIFICA CONFIGURAÇÃO DO VISUAL DO FIREFOX

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
        banco.Robo.Log.grava(txt,vida,f'{config.softer_name}')                                  # * SALVA O LOG NO BANCO DE DADOS
        nome_arquivo_log =f'c:/Sistemas/Robos/{config.softer_name}_{config.softer_version}/to_screen'
        arquivo_log = open(nome_arquivo_log,'a')                                                # * SALVA O LOG LOCALMENTE NA MÁQUINA
        print (registro, file=arquivo_log)                                                      # * 
        arquivo_log.close()                                                                     # * 
        
        registro_dtm = str(datetime.now().strftime('%Y%m%d'))                                   # * 
        nome_arquivo_log2 =f'c:/Sistemas/Robos/{config.softer_name}_{config.softer_version}/Log_{config.softer_name}_{registro_dtm}.txt'
        arquivo_log2 = open(nome_arquivo_log2,'a')                                              # * SALVA O LOG LOCALMENTE NA MÁQUINA
        print (registro, file=arquivo_log2)                                                     # * 
        arquivo_log2.close()                                                                    # * 
        pass
    
    def apaga_logs(self):
        '''Limpa os arquivos de logs mais antigos'''
        list_arquivos_log = glob('Log_' + config.softer_name + '*')                        # * LISTA OS ARQUIVOS DE LOGS EXISTENTES NA PASTA
        for for_arquivo_log in list_arquivos_log:                                               # * PARA CADA ARQUIVO FAZ A VERIFICAÇÃO
            data_arquivo = for_arquivo_log.split(config.softer_name)[1]
            data_arquivo = datetime.strptime(data_arquivo,'%Y%m%d.txt')
            if data_arquivo < datetime.now() - timedelta(days=8):                               # * SE FOR MAIS ANTIGO QUE OS DIAS ESTIPULADOS, APAGA O ARQUIVO
                os.remove(for_arquivo_log)
            else:
                pass       
        banco.Robo.Log.apaga()                                                                  # * LIMPA LOGS ANTIGOS NO BANCO DE DADOS        

    def decripta(self,texto):
            """
            Função que descriptografa senha do gestor para poder acessar o sigal
            """
            global PASSPHRASE
            PASSPHRASE = b'25b890c6103dbc87e533eb0338fffc1f2adf6eab4c4873cfdd4f24c497d49704';
            try:
                key = binascii.unhexlify(PASSPHRASE)
                encrypted = json.loads(base64.b64decode(texto).decode('ascii'))
                encrypted_data = base64.b64decode(encrypted['data'])
                iv = base64.b64decode(encrypted['iv'])
                tag = base64.b64decode(encrypted['tag'])
                cipher = AES.new(key, AES.MODE_GCM, iv)
                decrypted = cipher.decrypt_and_verify(encrypted_data, tag)
                return json.loads(base64.b64decode(decrypted).decode('ascii'))
            except:
                return 'Erro ao decriptar'
    
    def encrypta_fernet(self,senha):
        key = b'N-nMdHttV7-iyB_FxR9Q5NlfkEd1QGp12iVfn-RPEZY='
        f = Fernet(key)
        enc = f.encrypt(senha.encode())
        enc = str(str(enc).replace("b'", "")).replace("'",'')
        return enc

    def decrypta_fernet(self,senha):
        key = b'N-nMdHttV7-iyB_FxR9Q5NlfkEd1QGp12iVfn-RPEZY='
        f = Fernet(key)    
        dec = f.decrypt(senha)
        dec = str(str(dec).replace("b'", "")).replace("'",'')
        return dec

    def lista_contratos(idContratoGestor):
        lista = []
        for i in idContratoGestor:
            lista.append(i[0])
        return lista
    
    def inicia_navegador(self):
        self.registrando('Iniciando Navegador... isto pode demorar um pouco...','BLUE','SEMANA')
        try:
            start_naveg = self.sigal.start_webdriver(self.modo_navegador)                                               
            if start_naveg == 'erro':   self.result_start_naveg = 'falha'
            else:                       
                self.result_start_naveg = 'sucesso'
                self.cont_feedback = False
        except: self.result_start_naveg = 'falha'

        if self.result_start_naveg == 'falha':
            self.registrando('ATENÇÃO: Antivírus possivelmente está em execução!'   ,'RED','DIA')
            self.registrando('Falha ao iniciar o navegador, tentarei novamente...'  ,'RED','MES')

            lista_pids_filhos   = []
            pid_principal = os.getpid()
            cadeia_de_processos = psutil.Process(pid_principal)
            for processo in cadeia_de_processos.children(recursive=True):
                if processo.pid not in lista_pids_filhos: 
                    lista_pids_filhos.append(processo.pid)

            for pid in lista_pids_filhos:
                # os.system(f'taskkill /pid {str(pid)} /F')
                subprocess.Popen(f'taskkill /pid {str(pid)} /F', shell=True)
            lista_pids_filhos   = []

            self.inicia_navegador()
        pass

    def continuous_feedback(self,tempo=30,vezes=10):
        while self.cont_feedback == True :
            if vezes <= 0 : self.cont_feedback = False
            self.registrando('Por favor aguarde...','BLACK','DIA')
            vezes -=1
            sleep(tempo)

    def verify_update(self):
        list_new_versions =  banco.Robo.Versionamento.list_new_versions()
        if list_new_versions == None: return 'Erro ao buscar novas versões'
        if len(list_new_versions) == 0: return 'Não existe novas atualizações'
        else:
            update_obrigatorio  = 0
            for version in list_new_versions:
                obrigatorio = version[4]
                if obrigatorio == True: update_obrigatorio = 1 
            if update_obrigatorio == 1: return 'Existe uma atualização obrigatória, atualize antes de continuar'
            else: return 'Existe uma nova versão disponivel'

    def rotina_reset_senha(self):
        if self.cfg_reset == "ativo":
            for i in self.contrato_reset_atual:
                if int(i) == 7 : nome_Contrato = 'CURITIBA'                                                             # * 
                if int(i) == 22: nome_Contrato = 'OLINDA'                                                               # * RENOMEIA OS CODIGOS DOS CONTRATOS PARA OS SEUS NOMES
                if int(i) == 23: nome_Contrato = 'COLOMBO'                                                              # * PARA QUE O FEEFBACK AO USUÁRIO FIQUE MAIS AMIGÁVEL
                if int(i) == 24: nome_Contrato = 'JUIZFORA'                                                             # * 
                lista_matriculas_reset = banco.Siadm.seleciona_matriculas_reset(i)                                      # * VERIFICA NO BANCO DE DADOS SE EXISTEM MATRICULAS PARA RESETAR
                if len(lista_matriculas_reset) == 0:
                    self.registrando(f'{nome_Contrato} não possui matriculas para resetar')
                else:                                                                                                   # * CASO EXISTAM MATRICULAS NO BANCO DE DADOS PARA RESETAR
                    self.registrando(f'{nome_Contrato} tem {len(lista_matriculas_reset)} matrículas para resetar','BLUE','SEMANA')
                    # self.login_contrato = self.sigal.login(self.matGestor,self.senhaGestor)                                   # * ENTÃO FAZ O LOGON COM O GESTOR DO CONTRATO ATUAL
                    for item_reset in lista_matriculas_reset:                                                           # * PARA CADA RESET NA LISTA DE RESETS
                        resetar_matricula       = item_reset[0]                                                         # * MATRICULA QUE SE DESEJA RESETAR
                        solicitante             = item_reset[1]                                                         # * QUEM SOLICITOU QUE A MATRICULA SEJA RESETADA
                        if self.login_contrato == 'ok':                                                                      # * SE O LOGIN FOI REALIZADO COM SUCESSO
                            self.sigal.resetar_senha()                                                                  # * VAI PARA A PAGINA DO SIGAL QUE RESETA A SENHA
                            reset_de_senha = self.sigal.selecionar_matricula_reset(resetar_matricula)                   # * E RESETA A MATRICULA DESEJADA
                            if reset_de_senha == 'ok':                                                                  # * SE O RESET FOI BEM SUCEDIDO
                                banco.Siadm.atualiza_status_reset(resetar_matricula,1)                                  # * ATUALIZA ESTA INFORMAÇÃO NA TABELA DE REQUISIÇÕES DO SSAT
                                banco.Siadm.envia_email_solicitante(solicitante, resetar_matricula, 1)                  # * E ENVIA UM E-MAIL INFORMANDO O SUCESSO PARA O SOLICITANTE E PARA O USUÁRIO DA MATRICULA RESETADA
                                self.registrando (f'Resetado a matrícula {resetar_matricula}','GREEN','SEMANA')
                            else:                                                                                       # * E EM CASO DE FALHA NO RESET DE SENHA
                                banco.Siadm.atualiza_status_reset(resetar_matricula,2)                                  # * ATUALIZA ESTA INFORMAÇÃO NA TABELA DE REQUISIÇÕES DO SSAT, COM ERRO
                                banco.Siadm.envia_email_solicitante(solicitante, resetar_matricula, 2)                  # * E ENVIA UM E-MAIL INFORMANDO O ERRO PARA O SOLICITANTE
                                self.registrando (f'Falha no reset da matrícula {resetar_matricula}','RED','MES')
                        else:                                                                                           # * CASO ELE NÃO TENHA CONSEGUIDO FAZER LOGIN COM NENHUM GESTOR DO CONTRATO ELE TENTA NOVAMENTE MAIS TARDE
                            self.registrando (f'Tentarei resetar a matrícula {resetar_matricula} mais tarde.','RED','MES')      
            
        pass

    def rotina_cria_usuario(self):
        """
        1 - verifica quantidade de solicitação de usuário para criar
            2 - caso exista pega o top 1 e cadastra.
            3 - verifica se tem senhas para resetar
            4 - repete estes passos até haver 0 cadastros pendentes
        """
        if self.cfg_cadastro == "ativo":

            # BUSCANDO PRESTADORES PARA CADASTRO CONFORME MATRICULA GESTOR
            novos_funcionarios_para_cadastrar = banco.Siadm.novos_funcionarios_para_cadastrar(self.matGestor)
            # novos_funcionarios_para_cadastrar = banco.Siadm.novos_funcionarios_para_cadastrar('c143345')
            qt_novos_funcionarios_para_cadastrar = len(novos_funcionarios_para_cadastrar)
            self.registrando(f'Encontrado {qt_novos_funcionarios_para_cadastrar} funcionário(s) para cadastrar','BLACK','SEMANA')
            if qt_novos_funcionarios_para_cadastrar > 0:
                self.registrando(f'Cadastrando funcionário','BLACK','SEMANA')
                ###################################

                cadastro_atual = novos_funcionarios_para_cadastrar[0]

                cadastro_banco_funcionarioPk  = cadastro_atual.funcionario_pk
                cadastro_banco_nomePrestador  = cadastro_atual.nome
                cadastro_banco_funcionarioCpf = cadastro_atual.cpf.replace("-","").replace(".","")
                cadastro_banco_funcionarioRg  = cadastro_atual.rg.replace("-","").replace(".","")
                cadastro_banco_emissorRg      = cadastro_atual.emissor.replace("-","").replace(".","")
                cadastro_banco_nomeEmpresa    = cadastro_atual.NomeDaEmpresa
                cadastro_banco_contrato       = cadastro_atual.contrato
                cadastro_banco_un_vinculada   = cadastro_atual.Un_vinculada           

            
                self.registrando                            (f'Acessando menu','BLACK','SEMANA')
                self.sigal.cadastrar_prestador              ()
                self.registrando                            (f'Inserindo informações','BLACK','SEMANA')
                self.sigal.cad_pres_insert_informations     (cadastro_banco_un_vinculada    )
                self.registrando                            (f'CPF','BLACK','SEMANA')
                self.sigal.cad_pres_insert_cpf              (cadastro_banco_funcionarioCpf  )
                self.registrando                            (f'RG','BLACK','SEMANA')
                self.sigal.cad_pres_insert_rg               (cadastro_banco_funcionarioRg,cadastro_banco_emissorRg)
                self.registrando                            (f'Empresa','BLACK','SEMANA')
                self.sigal.cad_pres_defini_company          (cadastro_banco_nomeEmpresa     )
                self.registrando                            (f'Confirmando registro','BLACK','SEMANA')
                self.sigal.cad_pres_confirm_register        ()

                self.registrando(f'Obtendo protocolo','BLACK','SEMANA')
                cad_pres_numProtocolo = self.sigal.cad_pres_protService()

                if cad_pres_numProtocolo != False:
                    self.registrando(f'Gerado o protocolo: {cad_pres_numProtocolo}','BLACK','SEMANA')
                else:
                    self.registrando(f'Não consegui obter o protocolo','BLACK','SEMANA')

                self.registrando(f'Verificando sucesso','BLACK','SEMANA')

                cad_pres_finaliza = self.sigal.cad_pres_verify_sucess() 

                if (cad_pres_finaliza == True) and (cad_pres_numProtocolo != False):
                    self.registrando(f'Cadastrado com sucesso','BLACK','SEMANA')
                    banco.Siadm.InserirChamado(cad_pres_numProtocolo, cadastro_banco_funcionarioPk)
                    banco.Siadm.AtualizarSolicitacaoCadastro(1, cad_pres_numProtocolo, cadastro_banco_funcionarioPk)
                    banco.Siadm.inserirLogCadastro(
                        self.matGestor,
                        5,
                        'Concluido cadastro de prestador', 
                        cadastro_banco_funcionarioCpf, 
                        cadastro_banco_contrato, 
                        "NULL", 
                        "NULL")

                else:
                    self.registrando(f'Falha ao cadastrar','BLACK','SEMANA')

            
                ###################################
                self.rotina_reset_senha()
                self.rotina_cria_usuario()

            pass

    def rotina_libera_acesso_sistema(self):
        """
        1 - Verifica se existes solicitações de acesso pendentes
            2 - caso exista pega o top 1 e cadastra.
            3 - verifica se tem senhas para resetar
            4 - verifica se existe cadastros de usuário
            5 - repete estes passos até haver 0 liberações pendentes
        """
        if self.cfg_acesso == "ativo":

            list_liberar_acess_sistema = banco.Siadm.pendents_liberar_acess_sistema(self.matGestor)
            qt_liberar_acess_sistema = len(list_liberar_acess_sistema)


            self.registrando(f'Encontrado {qt_liberar_acess_sistema} acessos para liberar','BLACK','SEMANA')

            if qt_liberar_acess_sistema > 0:
                liberar_acesso_top_1 = list_liberar_acess_sistema[0] 

                continuar = 1

                liberar_banco_funcionarioPk     = liberar_acesso_top_1.funcionario_pk
                liberar_banco_nomePrestador     = liberar_acesso_top_1.nome
                liberar_banco_matPrestador      = liberar_acesso_top_1.matPrestador
                liberar_banco_sistemaPk         = liberar_acesso_top_1.sistema_acesso_pk
                liberar_banco_funcionarioCpf    = liberar_acesso_top_1.cpf
                liberar_banco_contrato          = liberar_acesso_top_1.contrato




                lista_sistemas_liberar = banco.Siadm.nomes_sistemas_liberar(self.matGestor,liberar_banco_matPrestador)
                sistema_liberar = lista_sistemas_liberar[0]
                # for sistema_liberar in lista_sistemas_liberar:
                
                liberar_sistema_nomeSistema     = sistema_liberar.nome_busca
                liberar_sistema_acessoSistemaPk = sistema_liberar.sistema_acesso_pk




                chk_mat_pres = liberar_banco_matPrestador
                if chk_mat_pres == None or chk_mat_pres =='None' or chk_mat_pres =='NULL':
                    self.registrando(f'Erro na matricula do prestador: {liberar_banco_matPrestador}','RED','MES')
                    continuar = 0

                if continuar == 1:
                    self.sigal.lib_aces_entra_menu()
                    select_mat_pres_liberar = self.sigal.lib_aces_seleciona_prestador(liberar_banco_matPrestador)
                    if select_mat_pres_liberar == "ok":
                        self.registrando(f'Selecionado Prestador: {liberar_banco_matPrestador}','BLACK','SEMANA')
                    else:                                   
                        self.registrando(f'Falha ao selecionar Prestador: {liberar_banco_matPrestador}','RED','MES')
                        
                        banco.Siadm.AtualizarSolicitacaoAcesso(
                            2, 
                            liberar_sistema_acessoSistemaPk, 
                            liberar_banco_matPrestador)

                        banco.Siadm.inserirLogAcess(
                            self.matGestor,
                            6,
                            "Cancelado liberação de acesso", 
                            liberar_banco_funcionarioCpf, 
                            liberar_banco_contrato, 
                            liberar_sistema_acessoSistemaPk, 
                            liberar_banco_matPrestador)                    
                        



                        self.sigal.close_session()

                        self.sigal = sigal.Sessao()                                                                                         # * INSTANCIA O MODULO DO SIGAL              
                        self.inicia_navegador()                                                                                             # * TENTA INICIAR O NAVEGADOR ATÉ OBTER SUCESSO          
                        self.login_contrato = self.sigal.login(self.matGestor,self.senhaGestor)




                        continuar == 0

                if continuar == 1:


                    add_sistema = self.sigal.lib_aces_carrinho_sistema(liberar_sistema_nomeSistema)

                    if add_sistema == 'ok':

                        banco.Siadm.AtualizarSolicitacaoAcesso(
                            1, 
                            liberar_sistema_acessoSistemaPk, 
                            liberar_banco_matPrestador)
                        
                        banco.Siadm.inserirLogAcess(
                            self.matGestor,
                            5,
                            "Concluído liberação de acesso", 
                            liberar_banco_funcionarioCpf, 
                            liberar_banco_contrato, 
                            liberar_sistema_acessoSistemaPk, 
                            liberar_banco_matPrestador)
                        
                        self.registrando(f'Solicitado: {liberar_sistema_nomeSistema}','BLACK','SEMANA')
                    
                    else:

                        banco.Siadm.AtualizarSolicitacaoAcesso(
                            2, 
                            liberar_sistema_acessoSistemaPk, 
                            liberar_banco_matPrestador)

                        banco.Siadm.inserirLogAcess(
                            self.matGestor,
                            6,
                            "Cancelado liberação de acesso", 
                            liberar_banco_funcionarioCpf, 
                            liberar_banco_contrato, 
                            liberar_sistema_acessoSistemaPk, 
                            liberar_banco_matPrestador)

                        self.registrando(f'Acesso já atribuido: {liberar_sistema_nomeSistema}','BLACK','SEMANA')

                        self.sigal.close_session()

                        self.sigal = sigal.Sessao()                                                                                         # * INSTANCIA O MODULO DO SIGAL              
                        self.inicia_navegador()                                                                                             # * TENTA INICIAR O NAVEGADOR ATÉ OBTER SUCESSO          
                        self.login_contrato = self.sigal.login(self.matGestor,self.senhaGestor)
                
                
                
                ##### * recursividade enquanto tiver demanda...
                self.sigal.resetar_senha()
                self.rotina_cria_usuario()
                self.rotina_libera_acesso_sistema()


        pass

    def rotina_remove_acesso_sistema(self):
        """
        1 - Verifica se existes solicitações de remoção de acesso pendentes
            2 - caso exista pega o top 1 e cadastra.
            3 - verifica se tem senhas para resetar
            4 - verifica se existe cadastros de usuário
            5 - Verifica se existes solicitações de acesso pendentes
            6 - repete estes passos até haver 0 liberações pendentes
        """
        if self.cfg_remocao == "ativo":

            inativa_pendents    = banco.Siadm.inativacoes_pendentes(self.matGestor)
            qt_inativa_pendents = len(inativa_pendents)
            self.registrando(f'Encontrado {qt_inativa_pendents} inativações para fazer','BLACK','SEMANA')

            if qt_inativa_pendents > 0:
                inativando_agora = inativa_pendents[0]

                inat_funcionarioCpf         = inativando_agora.cpf
                inat_matPrestador           = inativando_agora.matricula_inativacao
                inat_dt_cadastro            = inativando_agora.dt_cadastro
                inat_matricula_cadastro     = inativando_agora.matricula_cadastro
                inat_dt_aprovacao           = inativando_agora.dt_aprovacao
                inat_matricula_aprovacao    = inativando_agora.matricula_aprovacao
                inat_aprovacao              = inativando_agora.aprovacao
                inat_status                 = inativando_agora.status
                inat_id_contrato_siadm      = inativando_agora.id_contrato_siadm

                self.registrando(f'Inativando a matrícula: {inat_matPrestador}','BLACK','SEMANA')
                self.sigal.inativ_acess()
                if self.sigal.inativ_select_user(inat_matPrestador) == False:
                    self.registrando(f'Matricula não foi localizada no SIGAL','BLACK','SEMANA')
                    banco.Siadm.falha_ao_inativar(inat_matPrestador)
                else:
                    inativ_protocol = self.sigal.inativ_get_protocol()
                    if inativ_protocol == False:
                        self.registrando(f'Falha ao obter o protocolo da inativação','BLACK','SEMANA')
                    else:
                        self.registrando(f'Gerado protocolo de inativação: {inativ_protocol}','BLACK','SEMANA')
                        if self.sigal.inativ_verify_sucess() == True:
                            self.registrando(f'Sucesso ao inativar Matricula','BLACK','SEMANA')
                            banco.Siadm.save_prot_inativacao(inativ_protocol,inat_matPrestador)
                            banco.Siadm.insert_log_inativ(
                            self.matGestor
                            ,5
                            ,"Concluído inativação de matricula"
                            ,inat_funcionarioCpf
                            ,inat_id_contrato_siadm
                            ,inat_matPrestador
                            )
                        else:
                            self.registrando(f'Houve algum problema ao invalidar prestador!','BLACK','SEMANA')




                self.sigal.resetar_senha()
                self.rotina_cria_usuario()
                self.rotina_libera_acesso_sistema()
                self.rotina_remove_acesso_sistema()

        pass

    def controle_de_acoes(self):
        ''' * Função principal, responsável por orquestrar a rotina de reset de senhas'''

        if self.front_alive == True:
            self.registrando(f'Iniciando rotina {config.softer_version}','BLACK','SEMANA')

            self.idContratoGestor               = banco.Siadm.busca_contrato_SSAT(self.matGestor)
            self.contrato_reset_atual           = automacao.lista_contratos(self.idContratoGestor)
            
            self.idContratoGestor_SIADM         = banco.Siadm.busca_contrato_SIADM(self.matGestor)
            self.contrato_reset_atual_SIADM     = automacao.lista_contratos(self.idContratoGestor_SIADM)


            self.sigal = sigal.Sessao()                                                                                         # * INSTANCIA O MODULO DO SIGAL              
            self.cont_feedback = True                                                                                           # * DEIXA O FEEDBACK CONTINUO HABILITADO ATÉ A SEGUNDA ORDEM              
            Thread(target=self.continuous_feedback).start()                                                                     # * FAZ O FEEDBACK CONTINUO EM UM SUBTHREAD                                  
            self.inicia_navegador()                                                                                             # * TENTA INICIAR O NAVEGADOR ATÉ OBTER SUCESSO          

            self.login_contrato = self.sigal.login(self.matGestor,self.senhaGestor)

            self.proxima_exec = datetime.now()-timedelta(seconds=1)                                                             # * CONTROLE DE EXECUÇÃO DO ROBÔ
            while  self.front_alive == True:                                                                                   # * LOOP PERPÉTUO ENQUANTO A JANELA DO FRONT-END DO ROBÔ ESTIVER ABERTA
                if self.proxima_exec < datetime.now():                                                                          # * CASO ESTEJE DENTRO DO HORARIO DE EXECUÇÃO
                    self.rotina_reset_senha             ()
                    self.rotina_cria_usuario            ()
                    self.rotina_libera_acesso_sistema   ()
                    self.rotina_remove_acesso_sistema   ()

                    self.registrando (f'Sem mais ações no momento','BLUE','SEMANA')
                    self.proxima_exec = datetime.now()+timedelta(seconds=30)                                                    # * DEFINE A PROXIMA EXECUÇÃO DA ROTINA PARA DAQUI A 30 SEGUNDOS
                    self.sigal.resetar_senha()       ##### * para evitar que a sessão do sigal expire???
                sleep(2)                                                                                                        # * DORME 2 SEGUNDOS ANTES DE VER SE JÁ ESTÁ NA HORA DE EXECUTAR NOVAMENTE A ROTINA

    def check_alive(self):
        while self.front_alive == True:
            alter_front_alive = datetime.fromtimestamp(Path(config.front_alive_path).stat().st_mtime)
            if alter_front_alive < (datetime.now() - timedelta(seconds=3)): self.front_alive = False
            sleep(2)

automacao() # * FAZ A INVOCAÇÃO DA CASSE PRINCIPAL PARA A EXECUÇÃO DO ROBÔ





