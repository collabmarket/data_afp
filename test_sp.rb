require 'fileutils'
require_relative 'spensiones'

db = Spensiones.new
db.vc_excel(2016, 2016, 'A')
today = Time.now
day = 60*60*24

descargas = Dir.pwd + '/' + db.a0.conf.outdir + '/'
df = db.vc_df((today - 2*day).strftime("%Y-%m-%d"), 'A')
puts db.vc_table(1, 1)
puts 'df: Read from web'
df.write_csv(descargas + 'data.csv')
puts 'dfcsv: Read from csv'
dfcsv = Daru::DataFrame.from_csv descargas + 'data.csv'
puts "db list of methods: " + (db.methods - Object.methods).to_s + "\n"
puts "db.a0 list of methods: " + (db.a0.methods - Object.methods).to_s + "\n"
puts 'db.a0.quit: Close browser'
puts 'exit: Exit console'

Webdrone.irb_console
