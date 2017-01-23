from __future__ import print_function
import os
import glob
from datetime import datetime
from datatoolbox import logg_info, makedir

def rm_temp_files():
    for f in glob.glob("tmp/vcf*.csv"):
        os.remove(f)

# Si existe tmp/historical limpia csv historico
if os.path.exists('tmp/historical'):
    rm_temp_files()
    clean_hist = True
else:
    clean_hist = False

# Si existe tmp/year limpia csv historico
if os.path.exists('tmp/year'):
    rm_temp_files()
    clean_year = True
else:
    clean_year = False

year = datetime.now().year

def histcsv_files(year):
    lastyear = year - 1
    inityear = [2002, 2002, 1981, 2002, 2000]
    fondos = list('ABCDE')
    histcsv = ['vcf%s%s-%s.csv'%(i,iy,lastyear) 
                for i,iy in zip(fondos,inityear)]
    return histcsv

def yearcsv_files(year):
    fondos = list('ABCDE')
    return ['vcf%s%s-%s.csv'%(i,year,year) for i in fondos]

histcsv = histcsv_files(year)
yearcsv = yearcsv_files(year)

def fillheader(linea):
    ''' Crea un encabezado valido para pandas Multi-level index
    '''
    lista = linea.split(';')
    for i in range(2,len(lista),2):
        #Repite Nombre AFP
        lista[i] = lista[i-1]
    # Remueve "\n" final
    lista[-1] = lista[-1].replace('\n','')
    #Repite Nombre AFP final y agrega "\n"
    lista.append(lista[-1]+'\n')
    return ';'.join(lista)

def cleancsv(filecsv):
    ''' Separa en archivos csv validos
    '''
    file_name, file_ext = filecsv.split('.')
    
    with open('rawdata/'+filecsv, 'rU') as f_in:
        lines = f_in.readlines()
    # Enumera lineas en blanco que separan trozos de datos
    # Trozos tienen distintas AFP encabezados no homogeneos
    blanks = [i for (i, s) in enumerate(lines) if s == "\n"]
    
    for j in range(len(blanks)):
        # Crea archivos csv validos con trozos
        f_out = open('tmp/'+file_name+'_%s.'%j+file_ext, 'w')
        
        if j < len(blanks)-1:
            # Linea en blanco antes de encabezados, por eso
            # blanks[j]+1
            # Primera fila encabezado rellena espacios
            f_out.write(fillheader(lines[blanks[j]+1]))
            # Segunda fila encabezado hasta linea en blanco
            f_out.writelines(lines[blanks[j]+2:blanks[j+1]])
        else:
            # Primera fila encabezado rellena espacios
            f_out.write(fillheader(lines[blanks[j]+1]))
            # Ultimo trozo archivo no termina en linea en blanco
            f_out.writelines(lines[blanks[j]+2:])
        
        f_out.close()

def main():
    logg_info('cleancsv', tipo='INFO', status='INIT')
    # Crea carpeta temporal
    makedir('tmp')
    if clean_hist:
        for filecsv in histcsv:
            cleancsv(filecsv)
        # Exec ok
        logg_info('cleancsv historical', tipo='INFO', status='OK')
        # Remove msg to clean historical
        os.remove('tmp/historical')

    if clean_year:
        for filecsv in yearcsv:
            cleancsv(filecsv)
        # Exec ok
        logg_info('cleancsv year', tipo='INFO', status='OK')
        # Remove msg to clean year
        os.remove('tmp/year')
    logg_info('cleancsv', tipo='INFO', status='DONE')

if __name__ == "__main__":
    main()
