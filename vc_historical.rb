require 'fileutils'
require_relative 'spensiones'
require_relative 'datatoolbox'

# Exec INIT
thisfile = File.basename(__FILE__)
logg_info("#{thisfile}", tipo='INFO', status='INIT')

# Variables
db = Spensiones.new
lastyear = Time.now.year - 1
fondos = ['A', 'B', 'C', 'D', 'E']
inityear = {'A' => 2002, 'B' => 2002, 'C' => 1981, 'D' => 2002, 'E' => 2000}

# Nombres directorios
descargas = Dir.pwd + '/' + db.a0.conf.outdir + '/'
rawdata = Dir.pwd + '/rawdata/'
tmp = Dir.pwd + '/tmp'

# Descarga excel valores cuota historicos
for f in fondos
  db.vc_excel(inityear[f], lastyear, f)
end

# Espera 10 seg para que se descargen los archivos
db.a0.wait.time        10

#Crea directorio rawdata si no existe
makedir(rawdata, by=thisfile)

# Copia excel valores cuota historicos en rawdata
for f in fondos
  FileUtils.cp(descargas + "vcf#{f}#{inityear[f]}-#{lastyear}.csv", rawdata)
end

# Crea carpeta tmp
makedir(tmp, by=thisfile)

# Indica a cleancsv recrear archivos historicos
FileUtils.touch('tmp/historical')
logg_info("#{thisfile} touch msg to cleancsv", tipo='INFO', status='OK')

# Close Browser
db.a0.quit

# Exec DONE
logg_info("#{thisfile}", tipo='INFO', status='DONE')
