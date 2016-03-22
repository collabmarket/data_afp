require 'webdrone'
require 'fileutils'

a0 = Webdrone.create browser: :firefox, timeout: 10

def vc(a0, y, m, d, fondo)
  mes = {1 => 'Enero', 2 => 'Febrero', 3 => 'Marzo', 4 => 'Abril', 5 => 'Mayo', 6 => 'Junio', 7 => 'Julio', 8 => 'Agosto', 9 => 'Septiembre', 10 => 'Octubre', 11 => 'Noviembre', 12 => 'Diciembre'}
  url = 'http://www.spensiones.cl/safpstats/stats/apps/vcuofon/vcfAFP.php?tf=' + fondo
  a0.open.url         url
  a0.form.set         'aaaaVCF', y
  a0.form.set         'mmVCF', mes[m]
  a0.form.set         'ddVCF', d
  a0.mark.on          'Buscar'
  a0.clic.on          'Buscar'
  a0.wait.time        1
end


vc(a0, 2016, 02, 02, 'A')
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[1]'
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[1]'
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]'
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[3]'
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[1]'
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]'
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[3]'
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[1]'
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[2]'
a0.text.xpath '//*[@id="main"]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[3]'

a0.wait.time        10


Webdrone.irb_console
