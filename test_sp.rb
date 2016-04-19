require 'fileutils'
require_relative 'spensiones'

db = Spensiones.new
db.vc_excel(2016, 2016, 'A')
today = DateTime.parse(Time.now.utc.to_s) # date_range same timezone
lastday = db.vc_last('A')

descargas = Dir.pwd + '/' + db.a0.conf.outdir + '/'
df = db.vc_df(lastday.strftime("%Y-%m-%d"), 'A')
db.vc_df_head(lastday, 'A')
puts db.vc_table(1, 1)
puts 'df: Readed from web'
df.write_csv(descargas + 'data.csv')
puts 'dfcsv: Readed from csv'
dfcsv = Daru::DataFrame.from_csv descargas + 'data.csv'
puts "db list of methods: " + (db.methods - Object.methods).to_s + "\n"
puts "db.a0 list of methods: " + (db.a0.methods - Object.methods).to_s + "\n"
puts "Files downloaded in : " + descargas
puts 'db.a0.quit: Close browser'
puts 'exit: Exit console'

Webdrone.irb_console
