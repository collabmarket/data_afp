require 'webdrone'

a0 = Webdrone.create browser: :firefox, timeout: 10

def bajar_excel_spensiones(a0, yi, yf, fondo)
  url = 'http://www.spensiones.cl/safpstats/stats/apps/vcuofon/vcfAFP.php?tf=' + fondo
  a0.open.url         url
  a0.form.set         'aaaaini', yi
  a0.form.set         'aaaafin', yf
  a0.mark.on          'Genera'
  a0.clic.on          'Genera'
  a0.wait.time        1
end


bajar_excel_spensiones(a0, 2015, 2015, 'A')
bajar_excel_spensiones(a0, 2015, 2015, 'B')
bajar_excel_spensiones(a0, 2015, 2015, 'C')
bajar_excel_spensiones(a0, 2015, 2015, 'D')
bajar_excel_spensiones(a0, 2015, 2015, 'E')

Webdrone.irb_console
