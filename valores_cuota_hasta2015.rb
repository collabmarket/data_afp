require 'webdrone'
require 'fileutils'

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


bajar_excel_spensiones(a0, 2002, 2015, 'A')
bajar_excel_spensiones(a0, 2002, 2015, 'B')
bajar_excel_spensiones(a0, 1981, 2015, 'C')
bajar_excel_spensiones(a0, 2002, 2015, 'D')
bajar_excel_spensiones(a0, 2000, 2015, 'E')

a0.wait.time        10

descargas = 'J:/Descargas/'
rawdata = Dir.pwd + '/rawdata/'

FileUtils.mv(descargas + 'vcfA2002-2015.csv', rawdata)
FileUtils.mv(descargas + 'vcfB2002-2015.csv', rawdata)
FileUtils.mv(descargas + 'vcfC1981-2015.csv', rawdata)
FileUtils.mv(descargas + 'vcfD2002-2015.csv', rawdata)
FileUtils.mv(descargas + 'vcfE2000-2015.csv', rawdata)

#~ Webdrone.irb_console
