import glob
import os
import pandas as pd
from datetime import datetime

# Exec init
print "[INFO]--" + datetime.now().strftime('%Y-%M-%d %H:%M:%S') + "--" + "curator" + "--" + "INIT"


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

lista = [concat(vcfA).sort_index(), 
         concat(vcfB).sort_index(), 
         concat(vcfC).sort_index(), 
         concat(vcfD).sort_index(), 
         concat(vcfE).sort_index()]
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

# Prepara last month data
mdf = pd.read_csv('rawdata/month_data.csv', parse_dates=True,
                decimal=',', thousands='.', 
                index_col=['A.F.P.', 'Fondo', 'Fecha'])
mdf.rename(columns={'Valor Cuota ':'Valor Cuota',
                   'Valor Fondo ':'Valor Patrimonio'},
          inplace=True)
mdf.index.rename([u'AFP', u'Fondo', u'Fecha'], inplace=True)
# MultiIndex column equivalente a vc y pat
mdf = mdf.unstack(level=(0,1))


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
    # Agrega datos ultimo mes si afp estan en mdf
    if afp in mdf.columns.levels[1]:
        mvc = mdf.xs(('Valor Cuota',afp), axis=1, level=(0,1))
        vc = vc.append(mvc)
        mpat = mdf.xs(('Valor Patrimonio',afp), axis=1, level=(0,1))
        pat = pat.append(mpat)
    # Elimina datos duplicados
    vc = vc[~vc.index.duplicated(keep='last')]
    pat = pat[~pat.index.duplicated(keep='last')]
    # Ordena index
    vc.sort_index(inplace=True)
    pat.sort_index(inplace=True)
    # Crear los archivos csv
    vc.to_csv('data/VC-%s.csv'%afp_name)
    pat.to_csv('data/PAT-%s.csv'%afp_name)

# Exec ok
print "[INFO]--" + datetime.now().strftime('%Y-%M-%d %H:%M:%S') + "--" + "curator" + "--" + "DONE"
