# Run all the scripts

#~ load './vc_historical.rb'
load './vc_this_year.rb'
load './vc_this_month.rb'
%x( python cleancsv.py )
%x( python curator.py )

#~ Webdrone.irb_console
