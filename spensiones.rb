require 'webdrone'
require 'daru'

class Spensiones  
  attr_accessor :a0
  
  def initialize
    @a0 = Webdrone.create browser: :firefox, timeout: 10, error: :ignore
  end
  

  def vc_excel(yi, yf, fondo)
    url = 'http://www.spensiones.cl/safpstats/stats/apps/vcuofon/vcfAFP.php?tf=' + fondo
    @a0.open.url         url
    @a0.form.set         'aaaaini', yi
    @a0.form.set         'aaaafin', yf
    @a0.mark.on          'Genera'
    @a0.clic.on          'Genera'
    @a0.wait.time        1
  end
  
  def vc_date(date, fondo)
    y, m, d = date.split('-')
    mes = {1 => 'Enero', 2 => 'Febrero', 3 => 'Marzo', 4 => 'Abril', 
          5 => 'Mayo', 6 => 'Junio', 7 => 'Julio', 8 => 'Agosto', 
          9 => 'Septiembre', 10 => 'Octubre', 11 => 'Noviembre', 
          12 => 'Diciembre'}
    url = 'http://www.spensiones.cl/safpstats/stats/apps/vcuofon/vcfAFP.php?tf=' + fondo
    # URL of the current page
    curl = @a0.exec.script 'return location.href'
    @a0.open.url         url      if url != curl
    @a0.form.set         'aaaaVCF', y.to_i
    @a0.form.set         'mmVCF', mes[m.to_i]
    @a0.form.set         'ddVCF', d.to_i
    @a0.mark.on          'Buscar'
    @a0.clic.on          'Buscar'
    @a0.wait.time        1
  end
  
  def vc_table(i, j)
    timeout = @a0.conf.timeout
    @a0.conf.timeout = 1
    xp = "//*[@id=\"main\"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[#{i}]/td[#{j}]"
    aux = @a0.text.xpath xp
    # Warning: quita espacio final afecta tambien nombre columnas
    #aux = aux.rstrip
    @a0.conf.timeout = timeout
    return aux
  end
  
  def vc_df(date, fondo)
    # Marca fecha y fondo indicado
    vc_date(date, fondo)
    # Revisa si no existen datos retorna nil
    if(vc_table(1, 1).nil?)
      return nil
    end
    # Crea un df vacio
    df = Daru::DataFrame.new([], order: (1..3).to_a, index:(2..8).to_a)
    # Rellena el df con los datos
    for i in 1..3
      for j in 2..8
        df[i][j] = vc_table(j, i)
      end
    end
    # Renombrar columnas
    df.vectors = Daru::Index.new(df.row[2].to_a)
    # Borra fila con nombre columnas
    df.delete_row(2)
    # Agrega columnas con Fecha y tipo Fondo
    df.add_vector("Fecha", Array.new(6, date))
    df.add_vector("Fondo", Array.new(6, fondo))
    return df
  end
end


