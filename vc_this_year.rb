require 'fileutils'
require_relative 'spensiones'

db = Spensiones.new
year = Time.now.year
fondos = ['A', 'B', 'C', 'D', 'E']

# Descarga excel valores cuota presente año
for f in fondos
  db.vc_excel(year, year, f)
end

# Espera 10 seg para que se descargen los archivos
db.a0.wait.time        10

descargas = Dir.pwd + '/' + db.a0.conf.outdir + '/'
rawdata = Dir.pwd + '/rawdata/'

# Copia excel valores cuota presente año en rawdata
for f in fondos
  FileUtils.cp(descargas + "vcf#{f}#{year}-#{year}.csv", rawdata)
end


#~ Webdrone.irb_console
