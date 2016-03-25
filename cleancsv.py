import os

clean_hist = False
clean_year = True

histcsv = ['vcfA2002-2015.csv', 'vcfB2002-2015.csv', 
            'vcfC1981-2015.csv', 'vcfD2002-2015.csv', 
            'vcfE2000-2015.csv']

yearcsv = ['vcfA2016-2016.csv', 'vcfB2016-2016.csv', 
            'vcfC2016-2016.csv', 'vcfD2016-2016.csv', 
            'vcfE2016-2016.csv']

def maketmp():
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

def fillheader(linea):
    ''' Crea un encabezado valido para pandas Multi-level index
    '''
    lista = linea.split(';')
    for i in range(2,len(lista),2):
        lista[i] = lista[i-1] #Repite Nombre AFP
    lista[-1] = lista[-1].replace('\n','') # Remueve \n final
    lista.append(lista[-1]+'\n') #Repite Nombre AFP final y agrega \n
    return ';'.join(lista)

def cleancsv(filecsv):
    ''' Separa en archivos csv validos
    '''
    file_name, file_ext = filecsv.split('.')
    
    with open('rawdata/'+filecsv, 'r') as f_in:
        lines = f_in.readlines()
    # Enumera lineas en blanco que separan trozos de datos
    # Trozos tienen distintas AFP encabezados no homogeneos
    blanks = [i for (i, s) in enumerate(lines) if s == "\n"]
    # Crea carpeta temporal
    maketmp()
    
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
    if clean_hist:
        for filecsv in histcsv:
            cleancsv(filecsv)
    if clean_year:
        for filecsv in yearcsv:
            cleancsv(filecsv)

if __name__ == "__main__":
    main()
