require 'fileutils'
require_relative 'spensiones'

# Exec init
puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" + 
     "vc_historical" + "--" +"INIT"

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

#Crea directorio rawdata
if not File.exist?(rawdata)
  FileUtils.mkdir(rawdata)
  puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" +
  "vc_historical mkdir rawdata" + "--" +"OK"
end

# Copia excel valores cuota historicos en rawdata
for f in fondos
  FileUtils.cp(descargas + "vcf#{f}#{inityear[f]}-#{lastyear}.csv", rawdata)
end

# Crea carpeta tmp
if not File.exist?('tmp')
  FileUtils.mkdir('tmp')
  puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" +
  "vc_historical mkdir tmp" + "--" +"OK"
end

# Indica a cleancsv recrear archivos historicos
FileUtils.touch('tmp/historical')
puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" +
     "vc_historical touch msg to cleancsv" + "--" +"OK"

# Close Browser
db.a0.quit

# Exec ok
puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" + 
     "vc_historical" + "--" +"DONE"
