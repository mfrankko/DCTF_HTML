import pandas as pd
from bs4 import BeautifulSoup

with open("C:\\Users\\sfran\\OneDrive\\Documents\\Excel\\Impressão da Declaração - 2004.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

codigos = ['5856-01', '2484-01', '5993-01', '6912-01', '0561-07', '1708-06']

tables = soup.findAll("table")
tableMatrix = []
for table in tables:
    list_of_rows = []
    for row in table.findAll('tr'):
        list_of_cells = []
        for cell in row.findAll('td'):
            text = cell.text.replace('&nbsp;', '')
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)
    tableMatrix.append((list_of_rows, list_of_cells))

def find_index(l, c):
    for i, v in enumerate(l):
        if any(c in x for x in v):
            return i

index_codigos = [find_index(tableMatrix, codigo) for codigo in codigos]

dctf = []

def get_index(index):
    try:
        codigo = tableMatrix[index]
        codigo_1 = (codigo[1])
        codigo_2 = codigo_1[2]
        valor = tableMatrix[index + 2]
        valor_1 = valor[0]
        valor_2 = valor_1[0]
        valor_3 = valor_2[1]
        dctf.append((codigo_2, valor_3))
    except: pass

index_valores = [get_index(index_codigo) for index_codigo in index_codigos]
print(dctf)

df = pd.DataFrame(dctf)
df.columns = ['Código', 'Valor']
df.to_excel('C:\\Users\\sfran\\OneDrive\\Documents\\Excel\\name.xlsx', index=False)