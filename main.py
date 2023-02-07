import pandas as pd
from bs4 import BeautifulSoup
import os

dir_path = 'C:/Users/sfran/OneDrive/Documents/Excel/DCTFs'
html_list = []
for filename in os.listdir(dir_path):
     if filename.endswith('.html'):
        html_list.append(filename)

dctf = []
def extracao_dctf(html):
    f = open(f'C:\\Users\\sfran\\OneDrive\\Documents\\Excel\\DCTFs\\{html}')
    soup = BeautifulSoup(f, 'html.parser')
    tables = soup.findAll("table")

    codigos = ['5856-01', '2484-01', '5993-01', '6912-01', '0561-07', '1708-06', '0422-01', '1708-06', '0588-06'] #Lista de Códigos da RFB
    table_matrix = [] #Lista onde fica as informações extraídas do HTML num primeiro momento
    #dctf = [] #Lista onde fica os valores finais extraídos pela função get_index

    for table in tables:
        list_of_rows = []
        for row in table.findAll('tr'):
            list_of_cells = []
            for cell in row.findAll('td'):
                text = cell.text.replace('&nbsp;', '')
                list_of_cells.append(text)
            list_of_rows.append(list_of_cells)
        table_matrix.append((list_of_rows, list_of_cells))

    def find_index(l, c):
        for i, v in enumerate(l):
            if any(c in x for x in v):
                return i

    index_codigos = [find_index(table_matrix, codigo) for codigo in codigos]

    def get_index(index):
        try:
            codigo = table_matrix[index][1][2]
            debito = table_matrix[index + 2][0][0][1]
            pagamento = table_matrix[index + 2][0][2][1]
            compensacao = table_matrix[index + 2][0][3][1]
            dctf.append((codigo, debito, pagamento, compensacao))
        except: pass
    index_valores = [get_index(index_codigo) for index_codigo in index_codigos]

extracao = [extracao_dctf(html) for html in html_list]
df = pd.DataFrame(dctf)
df.columns = ['Código', 'Débito Apurado', 'Pagamento', 'Compensação']
df.to_excel('C:/Users/sfran/OneDrive/Documents/Excel/DCTFs/Compliance Obrigações Acessórias.xlsx', index=False)

