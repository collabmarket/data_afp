require 'fileutils'
require_relative 'spensiones'

# Exec init
puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" + 
     "vc_year" + "--" +"INIT"

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

#Crea directorio rawdata si no existe
if not File.exist?(rawdata)
  FileUtils.mkdir(rawdata)
  puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" +
  "vc_year mkdir rawdata" + "--" +"OK"
end

# Copia excel valores cuota presente agno en rawdata
for f in fondos
  FileUtils.cp(descargas + "vcf#{f}#{year}-#{year}.csv", rawdata)
end

# Crea carpeta tmp
if not File.exist?('tmp')
  FileUtils.mkdir('tmp')
  puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" +
  "vc_year mkdir tmp" + "--" +"OK"
end

# Indica a cleancsv recrear archivos year
FileUtils.touch('tmp/year')
puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" +
     "vc_year touch msg to cleancsv" + "--" +"OK"

# Close Browser
db.a0.quit

# Exec ok
puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" + 
     "vc_year" + "--" + "DONE"
