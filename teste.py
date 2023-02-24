from openpyxl import load_workbook


arquivo_xlsx = load_workbook('Dados.xlsx')
planilha = arquivo_xlsx['Contatos']

b = ws['D1'].value


print (b)


ws['D1'] = "modificghjgar"

wb.save('Dados.xlsx')





