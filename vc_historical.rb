require 'fileutils'
require_relative 'spensiones'

db = Spensiones.new
lastyear = Time.now.year - 1
fondos = ['A', 'B', 'C', 'D', 'E']
inityear = {'A' => 2002, 'B' => 2002, 'C' => 1981, 'D' => 2002, 'E' => 2000}

# Descarga excel valores cuota historicos
for f in fondos
  db.vc_excel(inityear[f], lastyear, f)
end

# Espera 10 seg para que se descargen los archivos
db.a0.wait.time        10

descargas = Dir.pwd + '/' + db.a0.conf.outdir + '/'
rawdata = Dir.pwd + '/rawdata/'

# Copia excel valores cuota historicos en rawdata
for f in fondos
  FileUtils.cp(descargas + "vcf#{f}#{inityear[f]}-#{lastyear}.csv", rawdata)
end

# Remueve la carpeta tmp, para que cleancsv recree archivos
FileUtils.rm_rf('tmp')
