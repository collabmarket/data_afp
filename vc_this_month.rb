require 'fileutils'
require_relative 'spensiones'

db = Spensiones.new
d = 60*60*24
today = Time.now
year = today.year
month = today.month
dby = (today - 2*d).day # day before yesterday
# Check last data
month_file = './rawdata/month_data.csv'
if File.exist?(month_file)
  # Fecha ultima linea de month_file
  # Warning: from_csv change headers order
  aux = Daru::DataFrame.from_csv './rawdata/month_data.csv'
  lastday = aux['Fecha'][-1]
  lyear, lmonth, lday = lastday.split('-').map(&:to_i)
else
  # Check and create df from two days ago
  aux = db.vc_df((today - 2*d).strftime("%Y-%m-%d"), 'A')
  # Delete data from aux only left headers
  for i in 3..8
    aux.delete_row(i)
  end
  lyear, lmonth, lday = [year, month, 0]
end

begin
  days = Daru::DateTimeIndex.date_range(
  :start => DateTime.new(lyear,lmonth,lday+1), 
  :end   => DateTime.new(year,month,dby), :freq => 'D').to_a
rescue Exception
  FileUtils.rm_f(month_file)
  exit(0)
end

fondos = ['A', 'B', 'C', 'D', 'E']

# Crea df para todos los fondos del presente mes
for f in fondos
  for day in days
    df = db.vc_df(day.strftime("%Y-%m-%d"), f)
    aux = aux.concat(df)
  end
end

descargas = Dir.pwd + '/' + db.a0.conf.outdir + '/'
rawdata = Dir.pwd + '/rawdata/'

# Escribe csv con valores cuota presente mes
aux.write_csv(descargas + 'month_data.csv')
# Copia df valores cuota presente mes en rawdata
FileUtils.cp(descargas + 'month_data.csv', rawdata)

# Remueve month_file, si cubre mas de un mes
FileUtils.rm_f(month_file) if days.length > 32 
