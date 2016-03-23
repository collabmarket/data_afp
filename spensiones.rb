require 'fileutils'
require 'webdrone'
require 'daru'

a0 = Webdrone.create browser: :firefox, timeout: 10

def bajar_excel(a0, yi, yf, fondo)
  url = 'http://www.spensiones.cl/safpstats/stats/apps/vcuofon/vcfAFP.php?tf=' + fondo
  a0.open.url         url
  a0.form.set         'aaaaini', yi
  a0.form.set         'aaaafin', yf
  a0.mark.on          'Genera'
  a0.clic.on          'Genera'
  a0.wait.time        1
end

def set_date(a0, date, fondo)
  y, m, d = date.split('-')
  mes = {1 => 'Enero', 2 => 'Febrero', 3 => 'Marzo', 4 => 'Abril', 5 => 'Mayo', 6 => 'Junio', 7 => 'Julio', 8 => 'Agosto', 9 => 'Septiembre', 10 => 'Octubre', 11 => 'Noviembre', 12 => 'Diciembre'}
  url = 'http://www.spensiones.cl/safpstats/stats/apps/vcuofon/vcfAFP.php?tf=' + fondo
  a0.open.url         url
  a0.form.set         'aaaaVCF', y.to_i
  a0.form.set         'mmVCF', mes[m.to_i]
  a0.form.set         'ddVCF', d.to_i
  a0.mark.on          'Buscar'
  a0.clic.on          'Buscar'
  a0.wait.time        1
end

def value(a0, i, j)
  xp = "//*[@id=\"main\"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[#{i}]/td[#{j}]"
  return a0.text.xpath xp
end

def get_data(a0, date, fondo)
  set_date(a0, date, fondo)
  df = Daru::DataFrame.new([], order: (1..3).to_a, index:(2..8).to_a)
  for i in 1..3
    for j in 2..8
      df[i][j] = value(a0, j, i)
    end
  end
  # Renombrar columnas
  df.vectors = Daru::Index.new(df.row[2].to_a)
  # Borra fila con nombre columnas
  df.delete_row(2)
  # Agrega columnas con Fecha y tipo Fondo
  df[:Fecha] = Array.new(6, date)
  df[:Fondo] = Array.new(6, fondo)
  return df
end

bajar_excel(a0, 2016, 2016, 'A')

descargas = Dir.pwd + '/' + a0.conf.outdir + '/'
df = get_data(a0, '2016-02-02', 'A')
df.write_csv(descargas + 'data.csv')
#~ index = Daru::DateTimeIndex.date_range(
  #~ :start => '2016-2-1', :periods => 20, :freq => 'D')

Webdrone.irb_console
