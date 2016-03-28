import glob
import os
import pandas as pd

vcfA = glob.glob("tmp/vcfA*.csv")
vcfB = glob.glob("tmp/vcfB*.csv")
vcfC = glob.glob("tmp/vcfC*.csv")
vcfD = glob.glob("tmp/vcfD*.csv")
vcfE = glob.glob("tmp/vcfE*.csv")

# Crea carpeta data
def makedata():
    if not os.path.exists('data'):
        os.makedirs('data')

# Concatena archivos con trozos agrega filas y columnas segun el caso
def concat(vcf):
    aux = pd.DataFrame()
    for f in vcf:
        df = pd.read_csv(f, delimiter=';', 
                     header=[0,1], index_col=0, 
                     parse_dates=True, decimal=',', thousands='.')
        aux = pd.concat([aux,df])
    # Agrega nombres a las columnas y el indice
    aux.columns.names = ['AFP', 'Item']
    aux.index.names = ['Fecha']
    return aux

lista = [concat(vcfA), concat(vcfB), concat(vcfC), 
         concat(vcfD), concat(vcfE)]
fondos = ['A', 'B', 'C', 'D', 'E']
# Crea carpeta data
makedata()
# Archivos de valor cuota y valor patrimonio un fondo todas las AFP
for aux,letra in zip(lista,fondos):
    aux.to_csv('data/f%s.csv'%letra)

# Archivos de valor cuota un fondo todas las AFP
# Archivos de valor patrimonio un fondo todas las AFP
for aux,letra in zip(lista,fondos):
    aux.xs('Valor Cuota', axis=1, level=1).to_csv('data/vcf%s.csv'%letra)
    aux.xs('Valor Patrimonio', axis=1, level=1).to_csv('data/patf%s.csv'%letra)

# Fondo C desde inicio tiene nombres de todas las AFP
afps = [i for i in lista[2].columns.levels[0]]

# Archivos de valor cuota de una AFP todos los fondos
# Archivos de valor patrimonio de una AFP todos los fondos
for afp in afps:
    vc = pd.DataFrame()
    pat = pd.DataFrame()
    for df,letra in zip(lista,fondos):
        # Verifica si la AFP esta en df
        if afp in df.columns.levels[0]:
            vc_aux = df[afp, 'Valor Cuota']
            vc_aux.name = letra
            pat_aux = df[afp, 'Valor Patrimonio']
            pat_aux.name = letra
            vc = pd.concat([vc, vc_aux], axis=1)
            pat = pd.concat([pat, pat_aux], axis=1)
    afp_name = afp.replace(' ', '-')
    # Elimina filas sin valores
    vc.dropna(how='all', inplace=True)
    pat.dropna(how='all', inplace=True)
    # Crear los archivos csv
    vc.to_csv('data/VC-%s.csv'%afp_name)
    pat.to_csv('data/PAT-%s.csv'%afp_name)

