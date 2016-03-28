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

dfA = concat(vcfA)
dfB = concat(vcfB)
dfC = concat(vcfC)
dfD = concat(vcfD)
dfE = concat(vcfE)

lista = [dfA, dfB, dfC, dfD, dfE]
letra = ['A', 'B', 'C', 'D', 'E']
makedata()
# Archivos de valor cuota y valor patrimonio un fondo todas las AFP
for aux,l in zip(lista,letra):
    aux.to_csv('data/f%s.csv'%l)

# Archivos de valor cuota un fondo todas las AFP
# Archivos de valor patrimonio un fondo todas las AFP
for aux,l in zip(lista,letra):
    aux.xs('Valor Cuota', axis=1, level=1).to_csv('data/vcf%s.csv'%l)
    aux.xs('Valor Patrimonio', axis=1, level=1).to_csv('data/patf%s.csv'%l)

# Archivos de valor cuota de una AFP todos los fondos
# Archivos de valor patrimonio de una AFP todos los fondos

# Fondo C desde inicio tiene nombres de todas las AFP
afps = [i for i in dfC.columns.levels[0]]
fondo = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E'}

for afp in afps:
    vc = pd.DataFrame()
    pat = pd.DataFrame()
    for i, df in enumerate(lista):
        if afp in df.columns.levels[0]:
            vc_aux = df[afp, 'Valor Cuota']
            vc_aux.name = fondo[i]
            pat_aux = df[afp, 'Valor Patrimonio']
            pat_aux.name = fondo[i]
            vc = pd.concat([vc, vc_aux], axis=1)
            pat = pd.concat([pat, pat_aux], axis=1)
    afp_name = afp.replace(' ', '-')
    # Elimina filas sin valores
    vc.dropna(how='all', inplace=True)
    pat.dropna(how='all', inplace=True)
    # Crear los archivos csv
    vc.to_csv('data/VC-%s.csv'%afp_name)
    pat.to_csv('data/PAT-%s.csv'%afp_name)

