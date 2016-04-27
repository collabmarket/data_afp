require 'fileutils'
require_relative 'spensiones'

# Exec init
puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" + 
     "vc_month" + "--" +"INIT"

db = Spensiones.new
lastday_sp = db.vc_last('A')
lmonth_sp = lastday_sp.month
lyear_sp = lastday_sp.year

# Check last data
rawdata = Dir.pwd + '/rawdata/'
month_file = rawdata + 'month_data.csv'
# TODO: Caso principio de agno
year_file = rawdata + "vcfA#{lyear_sp}-#{lyear_sp}.csv"

if File.exist?(year_file)
  # Read last line of year_file split and extract last day
  d = IO.readlines(year_file)[-1].split(";")[0]
  # Parse last day of year_file
  year_lastday = DateTime.strptime(d, '%Y-%m-%d')
else
  # Si no existe year_file ultimo dia mes anterior con datos spensiones
  year_lastday = DateTime.new(lyear_sp,lmonth_sp,1) - 1
end
 
if File.exist?(month_file)
  # Warning: from_csv change headers order
  aux = Daru::DataFrame.from_csv month_file
  # Busca datos incompletos
  aux_nan = aux.filter(:row) do |row|
            row.to_a.include? "-- "
            end
  # Fechas con datos incompletos
  fechas_nan = aux_nan['Fecha'].uniq.to_a
  # Elimina dias con datos incompletos
  aux =  aux.filter(:row) do |row|
         not fechas_nan.include? row['Fecha']
         end
  # Fecha primera y ultima linea de month_file
  firstday = DateTime.strptime(aux['Fecha'][0], '%Y-%m-%d')
  lastday = DateTime.strptime(aux['Fecha'][-1], '%Y-%m-%d')

  # Caso month_file tiene datos de mas de un mes
  # Elimina datos mes pasado cuando se agregan en vc_year
  if (year_lastday - firstday).to_i >= 0
    FileUtils.rm_f(month_file)
    aux = db.vc_df_head(lastday_sp, 'A')
    # inicio mes con datos spensiones
    inicio = DateTime.new(lyear_sp,lmonth_sp,1)

  # Caso month_file se puede actualizar
  else
    # inicio ultimo dia month_file mas 1
    inicio = DateTime.new(lastday.year,lastday.month,lastday.day+1)
  end

# Caso no existe month_file
else
  aux = db.vc_df_head(lastday_sp, 'A')
  # inicio mes
  inicio = DateTime.new(lyear_sp,lmonth_sp,1)
end

# Actualiza ultimo dia
if (lastday_sp - inicio).to_i == 0
  days = [lastday_sp]
# Caso month_file actualizado
elsif (lastday_sp - inicio).to_i == -1
  days = []
  puts "[INFO]--" + Time.now.strftime('%Y-%M-%d %H:%M:%S') + "--" + 
       "vc_month" + "--" + "UPDATED"
else
  begin
    # Caso month_file varios dias
    days = Daru::DateTimeIndex.date_range(
           :start => inicio, :end => lastday_sp, 
           :freq => 'D').to_a
  rescue Exception
    # Si existe un error no actualiza 
    days = []
    puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" + 
         "vc_month" + "--" + "FAILED"
  end
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

# Escribe csv con valores cuota presente mes
aux.write_csv(descargas + 'month_data.csv')
# Copia df valores cuota presente mes en rawdata
FileUtils.cp(descargas + 'month_data.csv', rawdata)

# Close Browser
db.a0.quit

# Exec ok
puts "[INFO]--" + Time.now.strftime('%Y-%m-%d %H:%M:%S') + "--" + 
     "vc_month" + "--" + "DONE"
