require 'fileutils'
require_relative 'spensiones'

db = Spensiones.new
db.vc_excel(2016, 2016, 'A')
today = Time.now
day = 60*60*24

descargas = Dir.pwd + '/' + db.a0.conf.outdir + '/'
df = db.vc_df((today - 2*day).strftime("%Y-%m-%d"), 'A')
print db.vc_table(1, 1)
df.write_csv(descargas + 'data.csv')

#~ index = Daru::DateTimeIndex.date_range(
  #~ :start => '2016-2-1', :periods => 20, :freq => 'D')

print "db list of methods: " + (db.methods - Object.methods).to_s + "\n"
print "db.a0 list of methods: " + (db.a0.methods - Object.methods).to_s + "\n"

Webdrone.irb_console
