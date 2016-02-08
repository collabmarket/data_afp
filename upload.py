import pandas as pd
import Quandl

# Read Quandl API Key from token.txt
with open('token.txt', 'r') as f:
    token = f.readline().rstrip('\n')

to_upload = ['CAPITAL', 'CUPRUM', 'HABITAT', 'MODELO', 'PLANVITAL', 'PROVIDA']

for afp in to_upload:
    df = pd.read_csv('data/VC-%s.csv'%afp, index_col=0, parse_dates=True)
    df.dropna(inplace=True) #Elimina filas con valor faltante
    codigo = 'VC_%s'%afp
    nombre =  'Valor Cuota %s'%afp
    Quandl.push(df, codigo, nombre, 
                desc=u'Descargados desde www.spensiones.cl', 
                authtoken=token, override=True, verbose=True)
