from openpyxl import load_workbook
import config



def gravar():
    arquivo_xlsx = load_workbook(f'{config.path_dir}/Dados.xlsx')
    planilha = arquivo_xlsx['Contatos']
    planilha['A2'] = '554599555633'
    planilha['A3'] = '554796959942'
    planilha['A4'] = '554797130128'
    planilha['A5'] = '556798849942'
    
    
    
    
    
    planilha['D2'] = ''
    planilha['D3'] = ''
    planilha['D4'] = ''
    planilha['D5'] = ''


    arquivo_xlsx.save(f'{config.path_dir}/Dados.xlsx')


# https://web.whatsapp.com/send?phone=5541984988524&text=HI

def visualizar():

    for item in range(4):

        arquivo_xlsx = load_workbook(f'{config.path_dir}/Dados.xlsx')
        planilha = arquivo_xlsx['Contatos']
    
        linha = item + 2
        fone    = planilha[f'A{linha}'].value
        nome    = planilha[f'B{linha}'].value
        texto   = planilha[f'C{linha}'].value
        status  = planilha[f'D{linha}'].value        
    
        print(f'{fone}---{nome}---{texto}---{status}')



# gravar()
visualizar()