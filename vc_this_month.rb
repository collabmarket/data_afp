require 'fileutils'
require_relative 'spensiones'

db = Spensiones.new
d = 60*60*24
today = Time.now
year = today.year
month = today.month

# Check last data
month_file = './rawdata/month_data.csv'
if File.exist?(month_file)
  # Fecha ultima linea de month_file
  # Warning: from_csv change headers order
  aux = Daru::DataFrame.from_csv './rawdata/month_data.csv'
  lastday = aux['Fecha'][-1]
  lyear, lmonth, lday = lastday.split('-').map(&:to_i)
else
  lyear, lmonth, lday = [0, 0, 0]
end
# Si month_file tiene datos del mes los usa
if year == lyear and month == lmonth
  # Lista de dias posteriores a month_file
  ## TODO revisar casos extremos
  days = (lday + 1)..(today - 2*d).day if today.day > 2
# En otro caso crea month_file desde dia 1
else
  days = 1..(today - 2*d).day if today.day > 2
  # Check and create df from two days ago
  aux = db.vc_df((today - 2*d).strftime("%Y-%m-%d"), 'A')
  # Delete data from aux only left headers
  for i in 3..8
    aux.delete_row(i)
  end
end

fondos = ['A', 'B', 'C', 'D', 'E']

# Crea df para todos los fondos del presente mes
for  f in fondos
  for day in days
    df = db.vc_df("#{year}-#{month}-#{day}", f)
    aux = aux.concat(df)
  end
end

descargas = Dir.pwd + '/' + db.a0.conf.outdir + '/'
rawdata = Dir.pwd + '/rawdata/'

# Escribe csv con valores cuota presente mes
aux.write_csv(descargas + 'month_data.csv')
# Copia df valores cuota presente mes en rawdata
FileUtils.cp(descargas + 'month_data.csv', rawdata)

#~ Webdrone.irb_console
