require 'fileutils'
require_relative 'spensiones'
require_relative 'datatoolbox'

# Variables
db = Spensiones.new
year = Time.now.year
fondos = ['A', 'B', 'C', 'D', 'E']

# Nombres directorios y archivos
descargas = Dir.pwd + '/' + db.a0.conf.outdir + '/'
rawdata = Dir.pwd + '/rawdata/'
tmp = Dir.pwd + '/tmp'
thisfile = File.basename(__FILE__)

# Exec init
logg_info("#{thisfile}", tipo='INFO', status='INIT')

# Descarga excel valores cuota presente año
for f in fondos
  db.vc_excel(year, year, f)
end

# Espera 10 seg para que se descargen los archivos
db.a0.wait.time        10

#Crea directorio rawdata si no existe
makedir(rawdata, by=thisfile)

# Copia excel valores cuota presente agno en rawdata
for f in fondos
  FileUtils.cp(descargas + "vcf#{f}#{year}-#{year}.csv", rawdata)
end

# Crea carpeta tmp
makedir(tmp, by=thisfile)

# Indica a cleancsv recrear archivos year
FileUtils.touch('tmp/year')
logg_info("#{thisfile} touch msg to cleancsv", tipo='INFO', status='OK')

# Close Browser
db.a0.quit

# Exec ok
logg_info("#{thisfile}", tipo='INFO', status='DONE')
