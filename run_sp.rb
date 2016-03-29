# Run all the scripts

#~ load './vc_historical.rb'
load './vc_this_year.rb'
load './vc_this_month.rb'
%x( python cleancsv.py )
%x( python curator.py )
%x( jupyter nbconvert --to notebook --execute A-E_AFP.ipynb )
%x( jupyter nbconvert --to notebook --execute ValoresCuotaAFP.ipynb )


#~ Webdrone.irb_console
