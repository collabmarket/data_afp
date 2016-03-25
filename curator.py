import glob
import os
import pandas as pd

vcfA = glob.glob("tmp/vcfA*.csv")
vcfB = glob.glob("tmp/vcfB*.csv")
vcfC = glob.glob("tmp/vcfC*.csv")
vcfD = glob.glob("tmp/vcfD*.csv")
vcfE = glob.glob("tmp/vcfE*.csv")

def makedata():
    if not os.path.exists('data'):
        os.makedirs('data')

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

# Archivos de valor cuota y valor patrimonio un fondo todas las AFP
dfA = concat(vcfA)
dfB = concat(vcfB)
dfC = concat(vcfC)
dfD = concat(vcfD)
dfE = concat(vcfE)


makedata()
dfA.to_csv('data/vcfA.csv')
dfB.to_csv('data/vcfB.csv')
dfC.to_csv('data/vcfC.csv')
dfD.to_csv('data/vcfD.csv')
dfE.to_csv('data/vcfE.csv')

vcfA = pd.read_csv('data/vcfA.csv', header=[0,1], index_col=0, parse_dates=True)
vcfB = pd.read_csv('data/vcfB.csv', header=[0,1], index_col=0, parse_dates=True)
vcfC = pd.read_csv('data/vcfC.csv', header=[0,1], index_col=0, parse_dates=True)
vcfD = pd.read_csv('data/vcfD.csv', header=[0,1], index_col=0, parse_dates=True)
vcfE = pd.read_csv('data/vcfE.csv', header=[0,1], index_col=0, parse_dates=True)

lista = [vcfA, vcfB, vcfC, vcfD, vcfE]
afps = [i for i in vcfC.columns.levels[0]]
fondo = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E'}

# Archivos de valor cuota de una AFP todos los fondos
# Archivos de valor patrimonio de una AFP todos los fondos

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
    vc.to_csv('data/VC-%s.csv'%afp_name)
    pat.to_csv('data/PAT-%s.csv'%afp_name)

