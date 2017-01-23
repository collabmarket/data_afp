from __future__ import print_function
import glob
import os
import pandas as pd
from datatoolbox import logg_info, makedir

# Exec init
logg_info('curator', status='INIT')

# Listado archivos cada fondo
vcfA = glob.glob("tmp/vcfA*.csv")
vcfB = glob.glob("tmp/vcfB*.csv")
vcfC = glob.glob("tmp/vcfC*.csv")
vcfD = glob.glob("tmp/vcfD*.csv")
vcfE = glob.glob("tmp/vcfE*.csv")

# Opciones escrituda de archivos csv
karg_csv = dict(sep=';', decimal=',')

# Concatena archivos con trozos agrega filas y columnas segun el caso
def concat(vcf):
    aux = pd.DataFrame()
    # Opciones lectura csv con Multi-level index
    karg_vcf = dict(delimiter=';', header=[0,1], index_col=0, 
                    parse_dates=True, decimal=',', thousands='.')
    for f in vcf:
        df = pd.read_csv(f, **karg_vcf)
        aux = pd.concat([aux,df])
    # Agrega nombres a las columnas y el indice
    aux.columns.names = ['AFP', 'Item']
    aux.index.names = ['Fecha']
    # Ordena segun index
    return aux.sort_index()

data = {'A': concat(vcfA), 'B': concat(vcfB), 'C': concat(vcfC), 
        'D': concat(vcfD), 'E': concat(vcfE)}
fondos = sorted(data.keys())

# Crea carpeta data
makedir('data')
# Recorre todos los fondos
for letra in fondos:
    aux = data[letra]
    # Archivos de VC y PAT un fondo todas las AFP
    csvfname = 'data/f%s.csv'%letra
    aux.to_csv(csvfname, **karg_csv)

col_names = zip(['vcf','patf'],['Valor Cuota','Valor Patrimonio'])
# Recorre todos los fondos
for letra in fondos:
    aux = data[letra]
    # Recorre VC y PAT
    for name, col in col_names:
        df = aux.xs(col, axis=1, level=1)
        # Archivos de VC un fondo todas las AFP
        # Archivos de PAT un fondo todas las AFP
        csvfname = 'data/%s%s.csv'%(name, letra)
        df.to_csv(csvfname, **karg_csv)

# Prepara last month data en mdf
karg_mdf = dict(parse_dates=True, decimal=',', thousands='.', 
                index_col=['A.F.P.', 'Fondo', 'Fecha'], 
                na_values='-- ')
mdf = pd.read_csv('rawdata/month_data.csv', **karg_mdf)
col_rename = {'Valor Cuota ':'Valor Cuota', 
              'Valor Fondo ':'Valor Patrimonio'}
mdf.rename(columns=col_rename, inplace=True)
mdf.index.rename([u'AFP', u'Fondo', u'Fecha'], inplace=True)
# MultiIndex column equivalente a vc y pat
mdf = mdf.unstack(level=(0,1))

# Fondo C tiene nombres de todas las AFP
afps = [i for i in data['C'].columns.levels[0]]

col_names = zip(['VC','PAT'],['Valor Cuota','Valor Patrimonio'])
# Recorre todas las AFP 
for afp in afps:
    # Recorre VC y PAT
    for name, col in col_names:
        df = pd.DataFrame()
        # Recorre todos los fondos
        for letra in fondos:
            aux = data[letra]
            # Verifica si la AFP esta en aux
            if afp in aux.columns.levels[0]:
                df_aux = aux[afp, col]
                df_aux.name = letra
                df = pd.concat([df, df_aux], axis=1)
        # Elimina filas sin valores
        df.dropna(how='all', inplace=True)
        # Agrega datos ultimo mes si afp estan en mdf
        if afp in mdf.columns.levels[1]:
            mdf_aux = mdf.xs((col,afp), axis=1, level=(0,1))
            df = df.append(mdf_aux)
        # Elimina datos duplicados
        df = df[~df.index.duplicated(keep='last')]
        # Ordena index
        df.sort_index(inplace=True)
        # Reemplaza espacios para nombre archivos
        afp_name = afp.replace(' ', '-')
        # Archivos de VC una AFP todos los fondos
        # Archivos de PAT una AFP todos los fondos
        csvfname = 'data/%s-%s.csv'%(name, afp_name)
        df.to_csv(csvfname, **karg_csv)

# Exec ok
logg_info('curator', status='DONE')
