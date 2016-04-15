import pandas_datareader.data as web
import Quandl
from datetime import datetime

with open('token.txt', 'r') as f:
    token = f.readline().rstrip('\n')
# Indicadores de Riesgo sistemico
dow = Quandl.get('BCB/UDJIAD1', authtoken=token)
wti = Quandl.get('EIA/PET_RWTC_D', authtoken=token)
fedrate = web.DataReader("FEDFUNDS", 'fred', start=datetime(1955,1,1))
# Riesgo de tipo de cambio (solo para mostrar el pobre uso de derivados en 2009)
usdclp = Quandl.get("CURRFX/USDCLP", authtoken=token)

# Guarda datos
outdir = 'data_quandl/'
dow.to_csv(outdir + 'dow.csv')
wti.to_csv(outdir + 'wti.csv')
fedrate.to_csv(outdir + 'fedrate.csv')
usdclp.to_csv(outdir + 'usdclp.csv')
