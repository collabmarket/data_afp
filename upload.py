import pandas as pd
import glob
import Quandl

# Read Quandl API Key from token.txt
with open('token.txt', 'r') as f:
    token = f.readline()

vcfA = pd.read_csv('data/vcfA.csv', header=[0,1], index_col=0, parse_dates=True)
vcfB = pd.read_csv('data/vcfB.csv', header=[0,1], index_col=0, parse_dates=True)
vcfC = pd.read_csv('data/vcfC.csv', header=[0,1], index_col=0, parse_dates=True)
vcfD = pd.read_csv('data/vcfD.csv', header=[0,1], index_col=0, parse_dates=True)
vcfE = pd.read_csv('data/vcfE.csv', header=[0,1], index_col=0, parse_dates=True)

lista = [vcfA, vcfB, vcfC, vcfD, vcfE]
afps = [i for i in vcfC.columns.levels[0]]
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
    vc.to_csv('data/VC-%s.csv'%afp_name)
    pat.to_csv('data/PAT-%s.csv'%afp_name)

