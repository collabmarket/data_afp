import glob
import os
import pandas as pd

vcfA = glob.glob("tmp/vcfA*.csv")
vcfB = glob.glob("tmp/vcfB*.csv")
vcfC = glob.glob("tmp/vcfC*.csv")
vcfD = glob.glob("tmp/vcfD*.csv")
vcfE = glob.glob("tmp/vcfE*.csv")

if not os.path.exists('data'):
    os.makedirs('data')

def concat(vcf):
    aux = pd.DataFrame()
    for f in vcf:
        df = pd.read_csv(f, delimiter=';', 
                     header=[0,1], index_col=0, 
                     parse_dates=True, decimal=',', thousands='.')
        aux = pd.concat([aux,df])
    return aux

def putnames(df):
    df.columns.names = ['AFP', 'Item']
    df.index.names = ['Fecha']
    return df

dfA = concat(vcfA)
dfB = concat(vcfB)
dfC = concat(vcfC)
dfD = concat(vcfD)
dfE = concat(vcfE)

dfA = putnames(dfA)
dfB = putnames(dfB)
dfC = putnames(dfC)
dfD = putnames(dfD)
dfE = putnames(dfE)

dfA.to_csv('data/vcfA.csv')
dfB.to_csv('data/vcfB.csv')
dfC.to_csv('data/vcfC.csv')
dfD.to_csv('data/vcfD.csv')
dfE.to_csv('data/vcfE.csv')
