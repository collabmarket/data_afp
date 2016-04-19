require 'fileutils'
require_relative 'spensiones'

# Exec init
puts Time.now.strftime('%Y-%M-%d %H:%M:%S') + "--" + "this_month" + "--" +"INIT"

db = Spensiones.new
today = DateTime.parse(Time.now.utc.to_s) # date_range same timezone
lastday_sp = db.vc_last('A')

# Check last data
month_file = './rawdata/month_data.csv'
if File.exist?(month_file)
  # Warning: from_csv change headers order
  aux = Daru::DataFrame.from_csv './rawdata/month_data.csv'
  # Fecha primera y ultima linea de month_file
  firstday = DateTime.strptime(aux['Fecha'][0], '%Y-%m-%d')
  lastday = DateTime.strptime(aux['Fecha'][-1], '%Y-%m-%d')
  # Caso month_file tiene datos de mas de un mes
  if (lastday-firstday).to_i >= 31
    FileUtils.rm_f(month_file)
    aux = db.vc_df_head(lastday_sp, 'A')
    # inicio mes
    inicio = DateTime.new(today.year,today.month,1)
  # Caso month_file se puede actualizar
  else
    # inicio ultimo dia month_file mas 1
    inicio = DateTime.new(lastday.year,lastday.month,lastday.day+1)
  end
else
  # Caso no existe month_file
  aux = db.vc_df_head(lastday_sp, 'A')
  # inicio mes
  inicio = DateTime.new(today.year,today.month,1)
end

begin
  days = Daru::DateTimeIndex.date_range(
  :start => inicio, :end => lastday_sp, :freq => 'D').to_a
rescue Exception
  # Caso month_file actualizado
  days = []
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

# Close Browser
db.a0.quit

# Exec ok
puts Time.now.strftime('%Y-%M-%d %H:%M:%S') + "--" + "this_month" + "--" + "DONE"
