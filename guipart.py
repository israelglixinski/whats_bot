from threading import Thread
from queue import Queue
from time import sleep
import customtkinter
import tkinter
import config
import motor
from os import remove, makedirs

class front:
    def __init__(self):
        self.cont_linhas = 1
        self.feedback           = Queue()
        self.app_win            = customtkinter.CTk()
        self.app_win.geometry("800x600")
        self.app_win.title(config.softer_name)
        # self.app_win.wm_iconbitmap('my_icon.ico')

        self.prepare_toScreen()

        self.top()
        self.frame_midle = customtkinter.CTkFrame(master=self.app_win)
        self.frame_midle.pack(padx=5, pady=5, fill='both', expand=True, side=tkinter.TOP)

        # self.left()
        self.right()
        self.down()
        
        Thread(target=self.periodic_call).start()
        Thread(target=self.verify_update).start()
        # self.verify_update()
        self.app_win.mainloop()

    ##### * ########################################################################################
    ##### * ########################################################################################
    ##### * FUNÇÕES BACKEND DO GUI
    ##### * ########################################################################################
    ##### * ########################################################################################
    
    def exec_top_btn_1(self):

        # chk_reset        = self.checkbox_1.get()
        # chk_cadastro     = self.checkbox_2.get()
        # chk_acesso       = self.checkbox_3.get()
        # chk_remocao      = self.checkbox_4.get()
        chk_visual          = self.checkbox_5.get()
        tmp_min             = self.top_entry_1.get()
        tmp_max             = self.top_entry_2.get()
        linha_ini           = self.top_entry_3.get()
        linha_fin           = self.top_entry_4.get()




        with open (f'{config.path_dir}/configs','w') as arquivo_config:
            # print(f'reset        ={chk_reset   }',file=arquivo_config)
            # print(f'cadastro     ={chk_cadastro}',file=arquivo_config)
            # print(f'acesso       ={chk_acesso  }',file=arquivo_config)
            # print(f'remocao      ={chk_remocao }',file=arquivo_config)
            print(f'visual       ={chk_visual  }',file=arquivo_config)
            print(f'tmp_min      ={tmp_min     }',file=arquivo_config)
            print(f'tmp_max      ={tmp_max     }',file=arquivo_config)
            print(f'linha_ini    ={linha_ini   }',file=arquivo_config)
            print(f'linha_fin    ={linha_fin   }',file=arquivo_config)


        senha = self.top_entry_1.get()
        Thread(target=lambda:motor.ignition(self.feedback,self.app_win,senha,'start_bot')).start()

    def exec_top_btn_2(self):
        Thread(target=lambda:motor.ignition(self.feedback,self.app_win,'   ','atualiza')).start()

    def prepare_toScreen(self):
        try: makedirs(config.path_dir)
        except:pass

        try:    remove(config.toScreen_path)
        except: pass
        with open(config.toScreen_path,'a') as arquivo: arquivo.write('...\n')

    def periodic_call(self):
        while self.feedback.qsize() > 0:
            msg = self.feedback.get()
            
            text = msg[0]
            self.feed_back_box.insert(tkinter.END,f'{text}\n')
            self.feed_back_box.see("end")

            try: 
                comando = msg[2]
                if comando == 'bloquear':
                    try:    self.top_btn_1  .configure(state='disabled')
                    except: pass
                    try:    self.top_btn_2  .configure(state='disabled')
                    except: pass
                    try:    self.top_entry_1.configure(state='disabled')
                    except: pass
                    try:    self.top_entry_2.configure(state='disabled')
                    except: pass
                    try:    self.top_entry_3.configure(state='disabled')
                    except: pass
                    try:    self.top_entry_4.configure(state='disabled')
                    except: pass
                    try:    self.checkbox_5 .configure(state='disabled')
                    except: pass
                
                
                
                
                if comando == 'desbloquear':
                    try:    self.top_btn_1  .configure(state='normal'   )
                    except: pass
                    try:    self.top_btn_2  .configure(state='normal'   )
                    except: pass
                    try:    self.top_entry_1.configure(state='normal'   )
                    except: pass
                    try:    self.top_entry_2.configure(state='normal'   )
                    except: pass
                    try:    self.top_entry_3.configure(state='normal'   )
                    except: pass
                    try:    self.top_entry_4.configure(state='normal'   )
                    except: pass
                    try:    self.checkbox_5 .configure(state='normal'   )
                    except: pass






            except:pass

            try:    
                progress        = msg[1]  
                total           = progress[0]
                update          = progress[1]
                valor_unitario  = 1/total
                valor_atual     = valor_unitario*update
                self.progressbar_down.set(valor_atual)
            except: pass  

        ##### * FEEDBACK COM BASE NO ARQUIVO
        arquivo = open(config.toScreen_path,'r')
        leitura_total = arquivo.readlines()
        new_cont_linhas = len(leitura_total)
        if new_cont_linhas != self.cont_linhas:
            novas_linhas = leitura_total[self.cont_linhas:]
            for linha in novas_linhas:
                linha = linha.replace('\n','')    
                self.feed_back_box.insert(tkinter.END,f'{linha}\n')
                self.feed_back_box.see("end")
            self.cont_linhas = new_cont_linhas
        arquivo.close()



        with open(config.front_alive_path,'w') as frnt_aliv: frnt_aliv.write(' ')
        self.app_win.after(100,self.periodic_call) # * ETERNA RECURSIVIDADE

    def  verify_update(self):
        pass

    def mandatory_update(self):
        try:    self.top_btn_1  .configure(state='disabled')
        except: pass
        try:    self.top_btn_2  .configure(state='disabled')
        except: pass
        try:    self.top_entry_1.configure(state='disabled')
        except: pass
        self.feed_back_box.insert(tkinter.END,f'Existe uma atualização obrigatória, iniciando instalação...\n')
        sleep(2)
        self.exec_top_btn_2()

    def optional_update(self):
        self.feed_back_box.insert(tkinter.END,f'Existe uma nova versão disponivel, para instalar click no botão "ATUALIZAR"\n')

        self.top_btn_2 = customtkinter.CTkButton(master=self.frame_top,text='Atualizar',command=self.exec_top_btn_2)
        self.top_btn_2.pack(padx=5,pady=5, side=tkinter.LEFT)

        pass

    ##### * ########################################################################################
    ##### * ########################################################################################
    ##### * CONSTRUTORES DOS ELEMENTOS FRONT END
    ##### * ########################################################################################
    ##### * ########################################################################################

    def top(self):
        self.frame_top      = customtkinter.CTkFrame(master=self.app_win, height=40)
        self.frame_top      .pack(padx=5, pady=5, fill='both', side=tkinter.TOP)

        self.top_labe_l     = customtkinter.CTkLabel(self.frame_top, text="Tempo MIN")
        self.top_labe_2     = customtkinter.CTkLabel(self.frame_top, text="Tempo MAX")
        self.top_entry_1    = customtkinter.CTkEntry(master=self.frame_top, placeholder_text="")
        self.top_entry_2    = customtkinter.CTkEntry(master=self.frame_top, placeholder_text="")
        self.top_btn_1      = customtkinter.CTkButton(master=self.frame_top,text='Iniciar Robô',command=self.exec_top_btn_1)
        self.checkbox_5     = customtkinter.CTkCheckBox(master=self.frame_top,text='Visualizar')

        self.top_labe_l     .pack(padx=5,pady=5, side=tkinter.LEFT)
        self.top_entry_1    .pack(pady=5,padx=5, side=tkinter.LEFT)
        self.top_labe_2     .pack(padx=5,pady=5, side=tkinter.LEFT)
        self.top_entry_2    .pack(pady=5,padx=5, side=tkinter.LEFT)
        self.checkbox_5     .pack(padx=5,pady=5, side=tkinter.RIGHT)
        self.top_btn_1      .pack(padx=5,pady=5, side=tkinter.RIGHT)

        self.frame_top2     = customtkinter.CTkFrame(master=self.app_win, height=40)
        self.frame_top2     .pack(padx=5, pady=5, fill='both', side=tkinter.TOP)

        self.top_labe_3     = customtkinter.CTkLabel(self.frame_top2, text="Linha Ini.      ")
        self.top_labe_4     = customtkinter.CTkLabel(self.frame_top2, text="Linha Fin.     ")
        self.top_entry_3    = customtkinter.CTkEntry(master=self.frame_top2, placeholder_text="")
        self.top_entry_4    = customtkinter.CTkEntry(master=self.frame_top2, placeholder_text="")
        
        self.top_labe_3    .pack(pady=5,padx=5, side=tkinter.LEFT)
        self.top_entry_3    .pack(pady=5,padx=5, side=tkinter.LEFT)
        self.top_labe_4    .pack(pady=5,padx=5, side=tkinter.LEFT)
        self.top_entry_4    .pack(pady=5,padx=5, side=tkinter.LEFT)
        
        self.top_entry_1.insert(0, "5")
        self.top_entry_2.insert(0, "30")
        self.top_entry_3.insert(0, "2")
        self.top_entry_4.insert(0, "50")


        #########################################################
        #########################################################
        #########################################################
        # self.checkbox_1     = customtkinter.CTkCheckBox(master=self.frame_top2, text='Reset')
        # self.checkbox_2     = customtkinter.CTkCheckBox(master=self.frame_top2, text='Cadastro')
        # self.checkbox_3     = customtkinter.CTkCheckBox(master=self.frame_top2, text='Acesso')
        # self.checkbox_4     = customtkinter.CTkCheckBox(master=self.frame_top2, text='Remoção')
        
        # self.checkbox_1     .grid(row=1, column=0, pady=(10, 10), padx=20, sticky="n")
        # self.checkbox_2     .grid(row=1, column=1, pady=(10, 10), padx=20, sticky="n")
        # self.checkbox_3     .grid(row=1, column=2, pady=(10, 10), padx=20, sticky="n")
        # self.checkbox_4     .grid(row=1, column=3, pady=(10, 10), padx=20, sticky="n")

        # self.checkbox_1.select()
        # self.checkbox_2.select()
        # self.checkbox_3.select()
        # self.checkbox_4.select()
        #########################################################
        #########################################################
        #########################################################




        
    def left(self):
        self.frame_left = customtkinter.CTkFrame(master=self.frame_midle)
        self.frame_left.pack(padx=5, pady=5, fill='both', side=tkinter.LEFT)

        self.left_labe_l = customtkinter.CTkLabel(self.frame_left, text="Description:")
        self.left_labe_l.pack(padx=5,pady=5)
        
        self.left_entry_1 = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="Write Me")
        self.left_entry_1.pack(pady=5, padx=5)

        self.left_btn_1 = customtkinter.CTkButton(master=self.frame_left,text='Action 1',command=self.exec_left_btn_1)
        self.left_btn_1.pack(padx=5,pady=5)

        self.left_btn_2 = customtkinter.CTkButton(master=self.frame_left,text='Action 2',command=self.exec_left_btn_1)
        self.left_btn_2.pack(padx=5,pady=5)

    def right(self):
        self.frame_right = customtkinter.CTkFrame(master=self.frame_midle)
        self.frame_right.pack(padx=5, pady=5, fill='both', side=tkinter.LEFT, expand=True)

        self.feed_back_box = customtkinter.CTkTextbox(master=self.frame_right)
        self.feed_back_box.pack(fill='both', expand=True)

    def down(self):
        self.frame_down = customtkinter.CTkFrame(master=self.app_win, height=20)
        self.frame_down.pack(padx=5, pady=5, fill='both', side=tkinter.TOP)        
        
        self.progressbar_down = customtkinter.CTkProgressBar(self.frame_down)
        self.progressbar_down.pack(fill='both')        
        self.progressbar_down.set(1)
        











