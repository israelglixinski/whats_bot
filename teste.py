from openpyxl import load_workbook



arquivo_xlsx = load_workbook(f'Dados.xlsx')
planilha = arquivo_xlsx['Contatos']


